"""Tests for tools/claude_setup.py, run on temporary directories only."""

import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path

TOOL = Path(__file__).resolve().parent.parent / "tools" / "claude_setup.py"
_spec = importlib.util.spec_from_file_location("claude_setup", TOOL)
setup = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(setup)

HOOKS_JSON = {
    "PostToolUse": [
        {"matcher": "Edit|Write", "hooks": [{"type": "command", "command": 'python3 "{{HOOKS_DIR}}/check.py"'}]}
    ]
}
USER_SETTINGS = {
    "model": "opus",
    "hooks": {"PostToolUse": [{"matcher": "Bash", "hooks": [{"type": "command", "command": "true"}]}]},
}


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def snapshot(root):
    return {p.relative_to(root).as_posix(): p.read_bytes() for p in sorted(root.rglob("*")) if p.is_file()}


class SetupTest(unittest.TestCase):
    def setUp(self):
        self.domains = Path(self.enterContext(tempfile.TemporaryDirectory())).resolve()
        self.claude = Path(self.enterContext(tempfile.TemporaryDirectory())).resolve()
        self.roadmap = self.domains / "roadmap"
        write(self.roadmap / "skills/roadmap/SKILL.md", "skill\n")
        write(self.roadmap / "skills/roadmap/references/a.md", "reference\n")
        write(self.roadmap / "skills/roadmap/evals/evals.json", "{}\n")
        write(self.roadmap / "skills/roadmap/scripts/__pycache__/x.pyc", "bytecode")
        write(self.roadmap / "agents/roadmap-auditor.md", "agent\n")
        write(self.roadmap / "hooks/check.py", "print()\n")
        write(self.roadmap / "hooks.json", json.dumps(HOOKS_JSON))
        write(self.claude / "settings.json", json.dumps(USER_SETTINGS))

    def run_setup(self, *args):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = setup.main(["--claude-dir", str(self.claude), "--domains-dir", str(self.domains), *args])
        return code, output.getvalue()

    def settings(self):
        return json.loads((self.claude / "settings.json").read_text(encoding="utf-8"))

    def state(self):
        return json.loads((self.claude / "my-claude-setup.json").read_text(encoding="utf-8"))


class Discovery(SetupTest):
    def test_maps_every_kind_and_skips_evals_and_pycache(self):
        self.assertEqual(set(setup.domain_files(self.roadmap)), {
            "skills/roadmap/SKILL.md",
            "skills/roadmap/references/a.md",
            "agents/roadmap-auditor.md",
            "hooks/roadmap/check.py",
        })

    def test_resolves_the_hooks_dir_placeholder(self):
        hooks = setup.domain_hooks(self.roadmap, self.claude)
        command = hooks["PostToolUse"][0]["hooks"][0]["command"]
        self.assertEqual(command, f'python3 "{self.claude}/hooks/roadmap/check.py"')

    def test_a_domain_without_hooks_json_has_no_hooks(self):
        (self.roadmap / "hooks.json").unlink()
        self.assertEqual(setup.domain_hooks(self.roadmap, self.claude), {})

    def test_invalid_hooks_json_is_an_error(self):
        write(self.roadmap / "hooks.json", "{")
        with self.assertRaises(setup.SetupError):
            setup.domain_hooks(self.roadmap, self.claude)

    def test_unit_is_the_top_entry_of_its_kind(self):
        self.assertEqual(setup.unit("skills/roadmap/references/a.md"), "skills/roadmap")
        self.assertEqual(setup.unit("agents/roadmap-auditor.md"), "agents/roadmap-auditor.md")


if __name__ == "__main__":
    unittest.main()
