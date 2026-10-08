#!/usr/bin/env python3
"""Show an iteration's runs for review, and save the reviewer's feedback.

Usage: viewer.py <iteration> [--previous <iteration>] [--static <file>] [--port N]

Builds one page from assets/viewer.html with every run that has a run.json, in the
iteration's order: the case's prompt, expected output and review items, the run's status,
figures, closing account, changes and output files, its grades, weak assertions and
checked claims, and the iteration's benchmark.json in a second tab. --previous adds, beside
each run, the earlier iteration's output files and feedback for the run of the same name.

With --static, writes the page to the file and exits; the page then saves no feedback, and
its Submit button downloads feedback.json for the reviewer to put in the iteration's
folder. Without it, serves the page on 127.0.0.1, at --port or a free port when that one is
taken, builds it again at each load, and writes the reviews to the iteration's
feedback.json as they are typed; it runs until stopped. It starts no session.

Exits 1 when the folder holds no iteration.json or no run to review.

Adapted from skill-creator's eval-viewer/generate_review.py
(https://github.com/anthropics/claude-plugins-official,
plugins/skill-creator/skills/skill-creator/eval-viewer/generate_review.py, plugin cache
fa59bc903774), under the Apache License 2.0, and modified: see NOTICE at the root of
my-claude-setup.
"""

import argparse
import base64
import json
import mimetypes
import sys
from functools import partial
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

TEMPLATE = Path(__file__).resolve().parent.parent / "assets" / "viewer.html"
PLACEHOLDER = "/*__EMBEDDED_DATA__*/"
FEEDBACK = "feedback.json"
PORT = 3117
IMAGES = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"}
FIGURES = ("cost_usd", "duration_s", "calls", "estimated_calls", "model", "effort", "models", "efforts",
           "claude_version", "refusals", "skill_reads")


class Refused(Exception):
    pass


def read_json(path, default=None):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def read_text(path):
    try:
        return Path(path).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""


def recorded_of(iteration):
    recorded = read_json(iteration / "iteration.json")
    if not isinstance(recorded, dict):
        raise Refused(f"no iteration.json in {iteration}: give an iteration's folder")
    return recorded


def run_names(recorded):
    return [f"{case}/{configuration}/run-{number}" for case in recorded["cases"]
            for configuration in recorded["configurations"] for number in range(1, recorded["runs"] + 1)]


def embed(path, relative):
    """One output file: text when it reads as UTF-8 without a NUL, an image by its
    extension, a download otherwise."""
    data = path.read_bytes()
    if path.suffix.lower() not in IMAGES or path.suffix.lower() == ".svg":
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            text = None
        if text is not None and "\0" not in text and path.suffix.lower() != ".svg":
            return {"path": relative, "type": "text", "content": text}
    mime = "image/svg+xml" if path.suffix.lower() == ".svg" else (
        mimetypes.guess_type(path.name)[0] or "application/octet-stream")
    kind = "image" if path.suffix.lower() in IMAGES else "binary"
    return {"path": relative, "type": kind, "data_uri": f"data:{mime};base64,{base64.b64encode(data).decode()}"}


def outputs_of(folder):
    outputs = folder / "outputs"
    if not outputs.is_dir():
        return []
    return [embed(path, path.relative_to(outputs).as_posix())
            for path in sorted(outputs.rglob("*")) if path.is_file()]


def feedback_of(iteration, warn=True):
    """{run: feedback} from the iteration's feedback.json, empty reviews left out."""
    path = iteration / FEEDBACK
    if not path.exists():
        return {}
    data = read_json(path)
    if not isinstance(data, dict) or not isinstance(data.get("reviews"), list):
        if warn:
            print(f"{path} cannot be read: the page starts without its reviews, and saving one replaces it",
                  file=sys.stderr)
        return {}
    return {r["run"]: r["feedback"] for r in data["reviews"] if isinstance(r, dict)
            and isinstance(r.get("run"), str) and isinstance(r.get("feedback"), str) and r["feedback"].strip()}


def runs_of(iteration, recorded):
    metadata = {case: read_json(iteration / case / "eval_metadata.json", {}) for case in recorded["cases"]}
    runs = []
    for name in run_names(recorded):
        case, configuration, number = name.split("/")
        folder = iteration / name
        record = read_json(folder / "run.json")
        if not isinstance(record, dict):
            continue
        case_data = metadata[case]
        runs.append({
            "name": name, "case": case, "configuration": configuration, "run": int(number.removeprefix("run-")),
            "folder": str(folder), "prompt": case_data.get("prompt", ""),
            "expected_output": case_data.get("expected_output", ""), "review": case_data.get("review", []),
            "status": record.get("status"), "reason": record.get("reason"),
            "figures": {key: record.get(key) for key in FIGURES},
            "response": read_text(folder / "response.md"),
            "changes": read_json(folder / "changes.json", {"added": [], "modified": [], "deleted": []}),
            "outputs": outputs_of(folder), "grading": read_json(folder / "grading.json"),
        })
    return runs


def collect(iteration, previous=None):
    """The page's data for the iteration; Refused when it holds no run to review."""
    iteration = Path(iteration).resolve()
    recorded = recorded_of(iteration)
    runs = runs_of(iteration, recorded)
    if not runs:
        raise Refused(f"no run to review in {iteration}: start its runs with run.py first")
    earlier = None
    if previous is not None:
        previous = Path(previous).resolve()
        before = recorded_of(previous)
        earlier = {"iteration": previous.name, "feedback": feedback_of(previous, warn=False),
                   "outputs": {run["name"]: run["outputs"] for run in runs_of(previous, before) if run["outputs"]}}
    return {"skill_name": recorded["skill_name"], "iteration": iteration.name, "model": recorded.get("model"),
            "effort": recorded.get("effort"), "configurations": recorded["configurations"], "runs": runs,
            "benchmark": read_json(iteration / "benchmark.json"), "feedback": feedback_of(iteration),
            "previous": earlier}


def page(data):
    """The page: the template with the data in place of its placeholder. Every `<` of the
    data is escaped, so that no text of a run can close the page's script."""
    text = json.dumps(data, ensure_ascii=False).replace("<", "\\u003c")
    return TEMPLATE.read_text(encoding="utf-8").replace(PLACEHOLDER, f"const EMBEDDED_DATA = {text};", 1)


def save_feedback(iteration, payload):
    """Write the reviews to the iteration's feedback.json; ValueError when their shape is wrong."""
    names = set(run_names(recorded_of(Path(iteration))))
    if not isinstance(payload, dict) or not isinstance(payload.get("reviews"), list):
        raise ValueError("expected an object with a `reviews` list")
    for review in payload["reviews"]:
        if not isinstance(review, dict) or not isinstance(review.get("feedback"), str):
            raise ValueError("each review needs `run` and `feedback`")
        if review.get("run") not in names:
            raise ValueError(f"no run named {review.get('run')!r} in the iteration")
    (Path(iteration) / FEEDBACK).write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
                                            encoding="utf-8")


class Handler(BaseHTTPRequestHandler):
    def __init__(self, iteration, previous, *args, **kwargs):
        self.iteration, self.previous = iteration, previous
        super().__init__(*args, **kwargs)

    def answer(self, code, body, kind):
        self.send_response(code)
        self.send_header("Content-Type", kind)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path not in ("/", "/index.html"):
            self.send_error(404)
            return
        try:
            body = page(collect(self.iteration, self.previous)).encode("utf-8")
        except Refused as error:
            self.answer(500, str(error).encode("utf-8"), "text/plain; charset=utf-8")
            return
        self.answer(200, body, "text/html; charset=utf-8")

    def do_POST(self):
        if self.path != "/api/feedback":
            self.send_error(404)
            return
        try:
            payload = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))))
            save_feedback(self.iteration, payload)
        except (ValueError, Refused) as error:
            self.answer(400, json.dumps({"error": str(error)}).encode("utf-8"), "application/json")
            return
        self.answer(200, b'{"ok": true}', "application/json")

    def log_message(self, format, *args):
        pass


def server(iteration, previous, port):
    """An HTTP server for the page on 127.0.0.1, at port or, when it is taken, a free one;
    not started."""
    handler = partial(Handler, Path(iteration).resolve(), Path(previous).resolve() if previous else None)
    try:
        return HTTPServer(("127.0.0.1", port), handler)
    except OSError:
        return HTTPServer(("127.0.0.1", 0), handler)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Show an iteration's runs for review, and save the feedback.")
    parser.add_argument("iteration", type=Path, help="the iteration's folder")
    parser.add_argument("--previous", type=Path, help="an earlier iteration, whose outputs and feedback are shown")
    parser.add_argument("--static", type=Path, metavar="FILE", help="write the page to FILE instead of serving it")
    parser.add_argument("--port", type=int, default=PORT, help=f"the port to serve on ({PORT})")
    args = parser.parse_args(argv)
    iteration = args.iteration.resolve()
    try:
        data = collect(iteration, args.previous)
    except Refused as error:
        print(error, file=sys.stderr)
        return 1
    if args.static:
        args.static.parent.mkdir(parents=True, exist_ok=True)
        args.static.write_text(page(data), encoding="utf-8")
        print(f"{args.static}: {len(data['runs'])} runs of {data['skill_name']}, {data['iteration']}")
        return 0
    http = server(iteration, args.previous, args.port)
    print(f"http://127.0.0.1:{http.server_address[1]}/ serves {len(data['runs'])} runs of {data['skill_name']}, "
          f"{data['iteration']}; reviews are saved to {iteration / FEEDBACK}. Stop it with Ctrl+C.", flush=True)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        http.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
