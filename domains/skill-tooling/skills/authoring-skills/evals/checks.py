"""Static checks specific to domains/skill-tooling/skills/authoring-skills.

The template rules are the roadmap skill's, loaded from its evals/checks.py so that one
source holds them; evals stay in this repository, so the import never ships.
"""

import importlib.util
from pathlib import Path

ROADMAP_CHECKS = Path(__file__).resolve().parents[4] / "roadmap/skills/roadmap/evals/checks.py"


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


roadmap = _load("roadmap_checks", ROADMAP_CHECKS)


def run(skill: Path):
    yield from roadmap.check_templates(skill)
