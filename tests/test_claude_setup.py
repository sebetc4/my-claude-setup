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


class EnableDisable(SetupTest):
    def test_enable_copies_the_domain(self):
        code, output = self.run_setup("enable", "roadmap")
        self.assertEqual(code, 0, output)
        self.assertEqual((self.claude / "skills/roadmap/SKILL.md").read_text(encoding="utf-8"), "skill\n")
        self.assertTrue((self.claude / "agents/roadmap-auditor.md").is_file())
        self.assertTrue((self.claude / "hooks/roadmap/check.py").is_file())
        self.assertFalse((self.claude / "skills/roadmap/evals").exists())
        self.assertFalse((self.claude / "skills/roadmap/scripts").exists())
        self.assertEqual(set(self.state()["domains"]["roadmap"]["files"]), set(setup.domain_files(self.roadmap)))

    def test_enable_merges_hooks_and_keeps_user_settings(self):
        self.run_setup("enable", "roadmap")
        settings = self.settings()
        self.assertEqual(settings["model"], "opus")
        groups = settings["hooks"]["PostToolUse"]
        self.assertEqual(groups[0], USER_SETTINGS["hooks"]["PostToolUse"][0])
        self.assertEqual(groups[1]["hooks"][0]["command"], f'python3 "{self.claude}/hooks/roadmap/check.py"')

    def test_enable_creates_a_missing_settings_file(self):
        (self.claude / "settings.json").unlink()
        code, output = self.run_setup("enable", "roadmap")
        self.assertEqual(code, 0, output)
        self.assertEqual(self.settings(), {"hooks": setup.domain_hooks(self.roadmap, self.claude)})

    def test_enable_backs_up_settings_before_changing_them(self):
        original = (self.claude / "settings.json").read_bytes()
        self.run_setup("enable", "roadmap")
        backups = list((self.claude / "backups/my-claude-setup").glob("settings-*.json"))
        self.assertEqual([b.read_bytes() for b in backups], [original])

    def test_enable_asks_for_a_restart_when_hooks_change(self):
        _, output = self.run_setup("enable", "roadmap")
        self.assertIn("restart Claude Code", output)

    def test_disable_restores_settings_and_removes_the_copies(self):
        before = self.settings()
        self.run_setup("enable", "roadmap")
        code, output = self.run_setup("disable", "roadmap")
        self.assertEqual(code, 0, output)
        self.assertEqual(self.settings(), before)
        self.assertFalse((self.claude / "skills/roadmap").exists())
        self.assertFalse((self.claude / "hooks/roadmap").exists())
        self.assertFalse((self.claude / "agents/roadmap-auditor.md").exists())
        self.assertTrue((self.claude / "skills").is_dir())
        self.assertEqual(self.state()["domains"], {})

    def test_disable_of_a_domain_not_enabled_fails(self):
        code, output = self.run_setup("disable", "roadmap")
        self.assertEqual(code, 1)
        self.assertIn("not enabled", output)

    def test_enable_of_an_unknown_domain_fails(self):
        code, output = self.run_setup("enable", "nope")
        self.assertEqual(code, 1)
        self.assertIn("no domain named 'nope'", output)

    def test_enable_without_a_domain_fails(self):
        code, output = self.run_setup("enable")
        self.assertEqual(code, 1)
        self.assertIn("D=<domain>", output)


class Conflicts(SetupTest):
    def assert_blocked(self, expected, *args):
        before = snapshot(self.claude)
        code, output = self.run_setup(*args)
        self.assertEqual(code, 1, output)
        self.assertIn(expected, output)
        self.assertEqual(snapshot(self.claude), before)

    def test_a_locally_modified_file_blocks(self):
        self.run_setup("enable", "roadmap")
        write(self.claude / "skills/roadmap/SKILL.md", "edited by hand\n")
        self.assert_blocked("skills/roadmap/SKILL.md: modified in", "update", "roadmap")

    def test_a_locally_removed_file_blocks(self):
        self.run_setup("enable", "roadmap")
        (self.claude / "agents/roadmap-auditor.md").unlink()
        self.assert_blocked("agents/roadmap-auditor.md: removed from", "update", "roadmap")

    def test_an_entry_not_installed_by_this_repository_blocks(self):
        write(self.claude / "skills/roadmap/other.md", "older copy\n")
        self.assert_blocked("skills/roadmap: already exists", "enable", "roadmap")

    def test_an_entry_owned_by_another_domain_blocks(self):
        write(self.domains / "other/skills/roadmap/SKILL.md", "clash\n")
        self.run_setup("enable", "roadmap")
        self.assert_blocked("skills/roadmap: installed by domain 'roadmap'", "enable", "other")

    def test_a_hook_changed_in_settings_blocks(self):
        self.run_setup("enable", "roadmap")
        settings = self.settings()
        settings["hooks"]["PostToolUse"][1]["matcher"] = "Write"
        write(self.claude / "settings.json", json.dumps(settings))
        self.assert_blocked("settings.json: a PostToolUse hook installed by 'roadmap'", "update", "roadmap")

    def test_invalid_settings_block_even_with_force(self):
        write(self.claude / "settings.json", "{")
        self.assert_blocked("invalid JSON", "enable", "roadmap")
        self.assert_blocked("invalid JSON", "--force", "enable", "roadmap")

    def test_force_overrides_a_conflict(self):
        self.run_setup("enable", "roadmap")
        write(self.claude / "skills/roadmap/SKILL.md", "edited by hand\n")
        code, output = self.run_setup("--force", "update", "roadmap")
        self.assertEqual(code, 0, output)
        self.assertEqual((self.claude / "skills/roadmap/SKILL.md").read_text(encoding="utf-8"), "skill\n")


if __name__ == "__main__":
    unittest.main()
