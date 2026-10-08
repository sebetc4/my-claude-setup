"""Unit test for the sample skill the evaluation scripts are checked on, under evals/sample/.

It lives with the evals rather than in the domain's tests: a run's copy of the repository
holds the skill without its evals folder, and its checks must pass there.
"""

import importlib.util
import tempfile
import unittest
from pathlib import Path

EVALS = Path(__file__).resolve().parent
SCRIPTS = EVALS.parent / "scripts"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


workspace = load("sample_workspace", SCRIPTS / "workspace.py")


class Sample(unittest.TestCase):
    def test_the_sample_builds_validates_and_passes_the_audit(self):
        build = load("sample_build", EVALS / "sample/build.py")
        audit = load("sample_audit", SCRIPTS / "audit.py")
        with tempfile.TemporaryDirectory() as tmp:
            skill = build.build(Path(tmp) / "repo")
            self.assertEqual([c["name"] for c in workspace.load(skill)["evals"]], ["decision-note", "nothing-follows"])
            self.assertEqual(audit.audit(skill), [])
            iteration = workspace.prepare(skill, runs=1, cases=["decision-note"])
            self.assertTrue((iteration / "decision-note/with_skill/run-1").is_dir())


if __name__ == "__main__":
    unittest.main()
