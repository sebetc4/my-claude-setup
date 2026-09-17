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

    def test_skips_hidden_files(self):
        write(self.roadmap / "skills/roadmap/.DS_Store", "junk")
        self.assertNotIn("skills/roadmap/.DS_Store", setup.domain_files(self.roadmap))


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

    def test_wrong_shaped_domain_hooks_json_blocks(self):
        write(self.roadmap / "hooks.json", json.dumps({"PostToolUse": {"matcher": "Edit", "hooks": []}}))
        self.assert_blocked("hooks must map each event", "enable", "roadmap")

    def test_settings_must_be_an_object(self):
        write(self.claude / "settings.json", "[]")
        self.assert_blocked("must be a JSON object", "enable", "roadmap")
        self.assert_blocked("must be a JSON object", "--force", "enable", "roadmap")

    def test_settings_hooks_shape_is_validated(self):
        write(self.claude / "settings.json", json.dumps({"hooks": {"PostToolUse": {"bad": 1}}}))
        self.assert_blocked("hooks must map each event", "enable", "roadmap")
        self.assert_blocked("hooks must map each event", "--force", "enable", "roadmap")

    def test_an_untracked_file_inside_a_managed_entry_blocks(self):
        self.run_setup("enable", "roadmap")
        write(self.roadmap / "skills/roadmap/notes.md", "new file\n")
        write(self.claude / "skills/roadmap/notes.md", "mine\n")
        self.assert_blocked(
            "skills/roadmap/notes.md: already exists and was not installed by this repository",
            "update", "roadmap")

    def test_invalid_domain_name_blocks(self):
        self.assert_blocked("invalid domain name", "enable", "..")
        self.assert_blocked("invalid domain name", "enable", "a/b")
        self.assert_blocked("invalid domain name", "enable", ".hidden")

    def test_a_symlink_in_the_target_path_blocks(self):
        target_dir = Path(self.enterContext(tempfile.TemporaryDirectory()))
        (self.claude / "skills").mkdir()
        (self.claude / "skills/roadmap").symlink_to(target_dir)
        self.assert_blocked(
            "skills/roadmap/SKILL.md: a path component is a symbolic link",
            "enable", "roadmap")
        self.assertEqual(list(target_dir.iterdir()), [])

    def test_force_overrides_a_conflict(self):
        self.run_setup("enable", "roadmap")
        write(self.claude / "skills/roadmap/SKILL.md", "edited by hand\n")
        code, output = self.run_setup("--force", "update", "roadmap")
        self.assertEqual(code, 0, output)
        self.assertEqual((self.claude / "skills/roadmap/SKILL.md").read_text(encoding="utf-8"), "skill\n")


class Update(SetupTest):
    def setUp(self):
        super().setUp()
        self.run_setup("enable", "roadmap")

    def test_copies_a_changed_file_and_removes_a_deleted_one(self):
        write(self.roadmap / "skills/roadmap/SKILL.md", "skill v2\n")
        (self.roadmap / "skills/roadmap/references/a.md").unlink()
        code, output = self.run_setup("update", "roadmap")
        self.assertEqual(code, 0, output)
        self.assertEqual((self.claude / "skills/roadmap/SKILL.md").read_text(encoding="utf-8"), "skill v2\n")
        self.assertFalse((self.claude / "skills/roadmap/references").exists())

    def test_replaces_changed_hooks(self):
        hooks = json.loads(json.dumps(HOOKS_JSON))
        hooks["PostToolUse"][0]["matcher"] = "Write"
        write(self.roadmap / "hooks.json", json.dumps(hooks))
        self.run_setup("update", "roadmap")
        matchers = [group["matcher"] for group in self.settings()["hooks"]["PostToolUse"]]
        self.assertEqual(matchers, ["Bash", "Write"])

    def test_without_a_domain_updates_every_enabled_domain(self):
        write(self.roadmap / "agents/roadmap-auditor.md", "agent v2\n")
        code, output = self.run_setup("update")
        self.assertEqual(code, 0, output)
        self.assertIn("roadmap: updated", output)
        self.assertEqual((self.claude / "agents/roadmap-auditor.md").read_text(encoding="utf-8"), "agent v2\n")

    def test_a_domain_not_enabled_cannot_be_updated(self):
        write(self.domains / "other/agents/x.md", "x\n")
        code, output = self.run_setup("update", "other")
        self.assertEqual(code, 1)
        self.assertIn("'other' is not enabled", output)

    def test_a_domain_gone_from_the_repository_is_left_in_place(self):
        (self.roadmap / "hooks.json").unlink()
        for path in sorted(self.roadmap.rglob("*"), reverse=True):
            path.unlink() if path.is_file() else path.rmdir()
        self.roadmap.rmdir()
        code, output = self.run_setup("update")
        self.assertEqual(code, 0, output)
        self.assertIn("make disable D=roadmap", output)
        self.assertTrue((self.claude / "skills/roadmap/SKILL.md").is_file())


class List(SetupTest):
    def status_of(self, name):
        _, output = self.run_setup("list")
        return {line.split()[0]: line.split()[1] for line in output.splitlines()}[name]

    def test_a_domain_never_enabled_is_off(self):
        self.assertEqual(self.status_of("roadmap"), "off")

    def test_an_enabled_domain_is_on(self):
        self.run_setup("enable", "roadmap")
        self.assertEqual(self.status_of("roadmap"), "on")

    def test_a_repository_change_makes_it_outdated(self):
        self.run_setup("enable", "roadmap")
        write(self.roadmap / "skills/roadmap/SKILL.md", "skill v2\n")
        self.assertEqual(self.status_of("roadmap"), "outdated")

    def test_a_hooks_change_makes_it_outdated(self):
        self.run_setup("enable", "roadmap")
        (self.roadmap / "hooks.json").unlink()
        self.assertEqual(self.status_of("roadmap"), "outdated")

    def test_a_local_change_makes_it_modified(self):
        self.run_setup("enable", "roadmap")
        write(self.roadmap / "skills/roadmap/SKILL.md", "skill v2\n")
        write(self.claude / "skills/roadmap/SKILL.md", "edited by hand\n")
        self.assertEqual(self.status_of("roadmap"), "modified")

    def test_pycache_and_hidden_domains_are_not_listed(self):
        (self.domains / "__pycache__").mkdir()
        (self.domains / ".hidden").mkdir()
        _, output = self.run_setup("list")
        self.assertNotIn("__pycache__", output)
        self.assertNotIn(".hidden", output)


class Versions(SetupTest):
    def row(self, name):
        _, output = self.run_setup("list")
        return next(line.split(None, 2) for line in output.splitlines() if line.split()[0] == name)

    def test_enable_records_the_version(self):
        write(self.roadmap / "VERSION", "1.0.0\n")
        self.run_setup("enable", "roadmap")
        self.assertEqual(self.state()["domains"]["roadmap"]["version"], "1.0.0")

    def test_list_shows_the_repository_version_of_a_domain_not_enabled(self):
        write(self.roadmap / "VERSION", "1.0.0\n")
        self.assertEqual(self.row("roadmap"), ["roadmap", "off", "1.0.0"])

    def test_list_shows_the_installed_version(self):
        write(self.roadmap / "VERSION", "1.0.0\n")
        self.run_setup("enable", "roadmap")
        self.assertEqual(self.row("roadmap"), ["roadmap", "on", "1.0.0"])

    def test_a_version_bump_alone_makes_it_outdated(self):
        write(self.roadmap / "VERSION", "1.0.0\n")
        self.run_setup("enable", "roadmap")
        write(self.roadmap / "VERSION", "1.1.0\n")
        self.assertEqual(self.row("roadmap"), ["roadmap", "outdated", "1.0.0 → 1.1.0"])

    def test_a_domain_without_version_has_no_version_column(self):
        self.run_setup("enable", "roadmap")
        self.assertEqual(self.row("roadmap"), ["roadmap", "on"])

    def test_an_invalid_version_blocks_without_writing(self):
        write(self.roadmap / "VERSION", "v1\n")
        before = snapshot(self.claude)
        code, output = self.run_setup("enable", "roadmap")
        self.assertEqual(code, 1)
        self.assertIn("is not a version of the form X.Y.Z", output)
        self.assertEqual(snapshot(self.claude), before)

    def test_list_reports_a_broken_version_and_keeps_going(self):
        write(self.roadmap / "VERSION", "1.0.0\n")
        write(self.domains / "other/agents/x.md", "agent\n")
        write(self.domains / "other/VERSION", "v1\n")
        self.assertEqual(self.row("roadmap"), ["roadmap", "off", "1.0.0"])
        other = self.row("other")
        self.assertEqual(other[:2], ["other", "broken"])
        self.assertIn("is not a version of the form X.Y.Z", other[2])

    def test_a_broken_version_still_blocks_enable_without_writing(self):
        write(self.domains / "other/agents/x.md", "agent\n")
        write(self.domains / "other/VERSION", "v1\n")
        before = snapshot(self.claude)
        code, output = self.run_setup("enable", "other")
        self.assertEqual(code, 1)
        self.assertIn("is not a version of the form X.Y.Z", output)
        self.assertEqual(snapshot(self.claude), before)


if __name__ == "__main__":
    unittest.main()
