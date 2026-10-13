"""Tests for tools/reviews.py, on review files written in a temporary directory."""

import contextlib
import importlib.util
import io
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("reviews_report", ROOT / "tools" / "reviews.py")
report = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(report)
reviewfile = report.reviewfile

SESSION = "aabb0fa1-f563-4ec2-8228-00c695fa7a0c"
NOISE = {"kind": "noise", "severity": "medium", "target": "domains/roadmap/hooks/session_resume.py",
         "fix": "Inject one line."}


def review(status="complete", session=SESSION, to="2026-09-26T21:46:03.000Z", version="1.1.1",
           findings=(), injected=3912):
    return {
        "review": 1, "status": status, "date": to[:10], "session": session, "project": "/p", "trigger": "hook",
        "slice": {"from": "2026-09-26T21:00:00.000Z", "to": to},
        "tools": [{"id": "hook:roadmap/session_resume.py", "domain": "roadmap", "version": version}],
        "measured": {"setup": {"hook:roadmap/session_resume.py":
                               {"runs": 1, "injected_chars": injected, "blocks": 0, "errors": 0}}},
        "findings": list(findings),
    }


class Report(unittest.TestCase):
    def setUp(self):
        root = Path(self.enterContext(tempfile.TemporaryDirectory())).resolve()
        self.reviews, self.domains = root / "reviews", root / "domains"
        (self.domains / "roadmap").mkdir(parents=True)
        (self.domains / "roadmap" / "VERSION").write_text("1.1.1\n", encoding="utf-8")
        self.count = 0

    def add(self, meta):
        self.count += 1
        path = self.reviews / f"{meta['date']}-{meta['session'][:8]}-r{self.count}.md"
        reviewfile.write_text(path, reviewfile.render(meta))

    def run_report(self, *options):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = report.main(["--reviews", str(self.reviews), "--domains", str(self.domains), *options])
        self.assertEqual(code, 0)
        return output.getvalue().splitlines()

    def test_no_review_yet(self):
        self.assertEqual(self.run_report()[0],
                         "0 reviews (0 complete, 0 skipped, 0 requested) · 0 sessions · 0 projects")

    def test_the_header_counts_reviews_sessions_and_projects(self):
        self.add(review())
        self.add(review(status="skipped", session="bbbbbbbb-0000-4000-8000-000000000000", to="2026-09-28T10:00:00.000Z"))
        self.assertEqual(self.run_report()[0],
                         "2 reviews (1 complete, 1 skipped, 0 requested) · 2 sessions · 1 projects · 2026-09-26 → 2026-09-28")

    def test_one_line_per_tool_with_its_median_cost(self):
        self.add(review(injected=1000))
        self.add(review(injected=3000, to="2026-09-27T10:00:00.000Z"))
        row = next(line for line in self.run_report() if line.startswith("hook:roadmap/session_resume.py"))
        self.assertEqual(row.split()[1:4], ["2", "0", "1.1.1"])
        self.assertTrue(row.endswith("2,000 chars injected"))

    def test_findings_are_grouped_most_recurrent_first(self):
        waste = {"kind": "waste", "severity": "high", "target": "domains/roadmap/skills/roadmap/SKILL.md", "fix": "Say less."}
        self.add(review(findings=[NOISE]))
        self.add(review(findings=[NOISE, waste], to="2026-09-27T10:00:00.000Z"))
        lines = self.run_report()
        start = lines.index("findings, most recurrent first")
        self.assertEqual(lines[start + 1], "  2×  noise  domains/roadmap/hooks/session_resume.py  medium  1.1.1")
        self.assertEqual(lines[start + 2], "      Inject one line.")
        self.assertTrue(lines[start + 3].startswith("  1×  waste  domains/roadmap/skills/roadmap/SKILL.md  high"))

    def test_a_newer_version_no_review_used_yet(self):
        self.add(review(findings=[NOISE]))
        (self.domains / "roadmap" / "VERSION").write_text("1.2.0\n", encoding="utf-8")
        self.assertIn("  1×  noise  domains/roadmap/hooks/session_resume.py  medium  1.1.1  1.2.0 not reviewed yet",
                      self.run_report())

    def test_a_finding_absent_from_the_reviews_of_a_newer_version(self):
        self.add(review(findings=[NOISE]))
        self.add(review(version="1.2.0", to="2026-09-27T10:00:00.000Z"))
        self.add(review(version="1.2.0", to="2026-09-28T10:00:00.000Z"))
        self.add(review(status="skipped", version="1.2.0", to="2026-09-29T10:00:00.000Z"))
        (self.domains / "roadmap" / "VERSION").write_text("1.2.0\n", encoding="utf-8")
        self.assertIn("  1×  noise  domains/roadmap/hooks/session_resume.py  medium  1.1.1  absent from 2 reviews of 1.2.0",
                      self.run_report())

    def test_errors_stale_requests_and_unreadable_files(self):
        self.add(review(status="requested", to="2026-01-01T00:00:00.000Z"))
        (self.reviews / "errors.log").write_text("t1 s1 ValueError: a\nt2 s2 KeyError: b\n", encoding="utf-8")
        (self.reviews / "broken.md").write_text("not a review\n", encoding="utf-8")
        lines = self.run_report()
        for line in ("hook errors: 2", "  last: t2 s2 KeyError: b", "requests no Stop came back to: 1",
                     "unreadable: broken.md"):
            self.assertIn(line, lines)

    def test_unreadable_files_do_not_stop_the_report(self):
        self.add(review())
        (self.reviews / "bytes.md").write_bytes(b"---\nreview: 1\n\xff\xfe\n---\n")
        reviewfile.write_text(self.reviews / "shape.md", reviewfile.render({**review(), "slice": "foo"}))
        lines = self.run_report()
        self.assertTrue(lines[0].startswith("1 reviews (1 complete"))
        self.assertIn("unreadable: bytes.md", lines)
        self.assertIn("unreadable: shape.md", lines)


class Archive(Report):
    def closed(self, **fields):
        meta = review(**fields)
        return {**meta, "closed": meta["slice"]["to"]}

    def archive_dir(self):
        return self.reviews / "archive" / datetime.now(timezone.utc).date().isoformat()

    def test_moves_the_closed_reviews_it_read_and_keeps_the_rest(self):
        self.add(self.closed(findings=[NOISE]))
        self.add(self.closed(status="skipped", to="2026-09-27T10:00:00.000Z"))
        self.add(review(status="requested", to="2026-09-28T10:00:00.000Z"))
        self.add(review(to="2026-09-28T11:00:00.000Z"))
        (self.reviews / "broken.md").write_text("not a review\n", encoding="utf-8")
        (self.reviews / "x.draft").write_text("{}", encoding="utf-8")
        (self.reviews / "errors.log").write_text("t1 s1 ValueError: a\n", encoding="utf-8")
        lines = self.run_report("--archive")
        self.assertIn("  1×  noise  domains/roadmap/hooks/session_resume.py  medium  1.1.1", lines)
        self.assertEqual(lines[-1], f"archived: 2 reviews into {self.archive_dir()}; 2 not closed kept")
        self.assertEqual(sorted(path.name for path in self.archive_dir().iterdir()),
                         ["2026-09-26-aabb0fa1-r1.md", "2026-09-27-aabb0fa1-r2.md"])
        self.assertEqual(sorted(path.name for path in self.reviews.iterdir() if path.is_file()),
                         ["2026-09-28-aabb0fa1-r3.md", "2026-09-28-aabb0fa1-r4.md", "broken.md", "errors.log", "x.draft"])

    def test_a_review_already_archived_under_its_name_stays(self):
        self.add(self.closed())
        self.add(self.closed(to="2026-09-27T10:00:00.000Z"))
        self.archive_dir().mkdir(parents=True)
        (self.archive_dir() / "2026-09-26-aabb0fa1-r1.md").write_text("earlier\n", encoding="utf-8")
        self.assertEqual(self.run_report("--archive")[-1],
                         f"archived: 1 review into {self.archive_dir()}; 0 not closed kept; "
                         "1 kept, its name already archived there")
        self.assertTrue((self.reviews / "2026-09-26-aabb0fa1-r1.md").is_file())

    def test_nothing_to_archive(self):
        self.assertEqual(self.run_report("--archive")[-1], "archived: no closed review")
        self.assertFalse((self.reviews / "archive").exists())

    def test_archived_reviews_leave_the_findings_and_the_saturation_and_stay_in_the_medians(self):
        for number in range(10):
            self.add(self.closed(to=f"2026-09-26T{number:02d}:00:00.000Z", injected=1000,
                                 findings=[NOISE] if number == 0 else []))
        listed = reviewfile.listed(self.reviews)
        self.assertTrue(reviewfile.saturated(listed, "hook:roadmap/session_resume.py", "1.1.1"))
        self.run_report("--archive")
        self.add(self.closed(to="2026-09-27T10:00:00.000Z", injected=4000))
        lines = self.run_report()
        self.assertIn("no finding yet", lines)
        self.assertFalse(reviewfile.saturated(reviewfile.listed(self.reviews), "hook:roadmap/session_resume.py", "1.1.1"))
        row = next(line for line in lines if line.startswith("hook:roadmap/session_resume.py"))
        self.assertEqual(row.split()[1:4], ["1", "0", "1.1.1"])
        self.assertTrue(row.endswith("1,000 chars injected"), row)
        self.assertEqual(len(reviewfile.archived(self.reviews)), 10)


if __name__ == "__main__":
    unittest.main()
