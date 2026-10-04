"""Tests for the skill audit: one skill per rule that breaks it, per the rule catalogue of
docs/decisions/2026-10-03-skill-audit-rules.md."""

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent / "skills/authoring-skills/scripts"
_spec = importlib.util.spec_from_file_location("skill_audit", SCRIPTS / "audit.py")
audit = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(audit)

CLEAN = ("name: demo", "description: Does a thing. Use when the user asks for the thing.")


class Case(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(self.enterContext(tempfile.TemporaryDirectory())).resolve()

    def skill(self, *lines, raw=None, body="Body.\n", name="demo"):
        root = self.tmp / name
        root.mkdir(parents=True, exist_ok=True)
        text = raw if raw is not None else "---\n" + "".join(line + "\n" for line in lines) + "---\n\n" + body
        (root / "SKILL.md").write_text(text, encoding="utf-8")
        return root

    def found(self, root, **options):
        return audit.audit(root, **options)

    def rules(self, root, **options):
        return [(p.rule, p.severity) for p in self.found(root, **options)]

    def only(self, root, rule, severity="error", **options):
        problems = self.found(root, **options)
        self.assertEqual([(p.rule, p.severity) for p in problems], [(rule, severity)], problems)
        return problems[0]


class Clean(Case):
    def test_a_clean_skill_has_no_problem(self):
        self.assertEqual(self.found(self.skill(*CLEAN)), [])
        self.assertEqual(self.found(self.skill(*CLEAN), portable=True), [])


class Frontmatter(Case):
    def test_f1_no_opening_line(self):
        problem = self.only(self.skill(raw="\n---\nname: demo\n---\nBody.\n"), "F1")
        self.assertEqual(problem.line, 1)

    def test_f2_never_closed(self):
        self.only(self.skill(raw="---\nname: demo\ndescription: x\n\nBody.\n"), "F2")

    def test_f3_yaml_that_only_a_lax_parser_reads(self):
        for line in ("description: It runs after: always.", "description: @file first",
                     "description: x\ndescription: y", "metadata:\n\tauthor: me", "description: \"never closed"):
            with self.subTest(line=line):
                root = self.skill("name: demo", line)
                problem = self.only(root, "F3")
                self.assertIn("drops every field", problem.message)

    def test_f3_names_the_line(self):
        self.assertEqual(self.only(self.skill("name: demo", "description: a: b"), "F3").line, 3)

    def test_f4_outside_the_subset(self):
        self.only(self.skill("name: demo", "description: &d Text"), "F4", "warning")

    def test_f5_not_a_mapping(self):
        self.only(self.skill("- name: demo"), "F5")

    def test_f6_unknown_field(self):
        problem = self.only(self.skill(*CLEAN, "tools: Read, Grep"), "F6")
        self.assertEqual(problem.line, 4)

    def test_f6_suggests_the_closest_field(self):
        problem = self.only(self.skill(*CLEAN, "disable-model-invokation: true"), "F6")
        self.assertIn("did you mean `disable-model-invocation`", problem.message)

    def test_f6_portable_knows_only_the_six_standard_fields(self):
        root = self.skill(*CLEAN, "disable-model-invocation: true")
        self.assertEqual(self.found(root), [])
        self.only(root, "F6", portable=True)

    def test_f7_wrong_type_or_value(self):
        for line in ("effort: extreme", "context: inline", "shell: zsh", "disable-model-invocation: maybe",
                     "metadata: just text", "allowed-tools: [Read, 3]", "hooks: [a]", "model: 5"):
            with self.subTest(line=line):
                self.only(self.skill(*CLEAN, line), "F7")

    def test_f7_a_name_typed_as_a_number(self):
        self.assertIn(("F7", "error"), self.rules(self.skill("name: 123", "description: x")))

    def test_f7_booleans_take_the_forms_the_harness_accepts(self):
        for value in ("true", "False", "yes", "On", "off", "1", "0", '"no"'):
            with self.subTest(value=value):
                self.assertEqual(self.found(self.skill(*CLEAN, f"user-invocable: {value}")), [])

    def test_f7_lists_and_strings(self):
        for line in ("allowed-tools: Read Grep", "allowed-tools: [Read, Grep]", "paths: \"src/**\"",
                     "arguments:\n  - issue\n  - branch"):
            with self.subTest(line=line):
                self.assertEqual(self.found(self.skill(*CLEAN, line)), [])

    def test_f8_portable_value_forms(self):
        for line in ("metadata:\n  version: 1", "allowed-tools: [Read, Grep]"):
            with self.subTest(line=line):
                root = self.skill(*CLEAN, line)
                self.assertEqual(self.found(root), [])
                self.only(root, "F8", portable=True)
        self.assertEqual(self.found(self.skill(*CLEAN, "allowed-tools: Read Grep"), portable=True), [])

    def test_f9_compatibility_length(self):
        for value in ('""', "x" * 501):
            with self.subTest(value=value[:10]):
                self.only(self.skill(*CLEAN, f"compatibility: {value}"), "F9")
        self.assertEqual(self.found(self.skill(*CLEAN, "compatibility: " + "x" * 500)), [])

    def test_f10_fork_only_fields(self):
        for line in ("agent: Explore", "background: false"):
            with self.subTest(line=line):
                self.only(self.skill(*CLEAN, line), "F10", "warning")
                self.assertEqual(self.found(self.skill(*CLEAN, "context: fork", line)), [])

    def test_f11_metadata_key_named_like_a_field(self):
        self.only(self.skill(*CLEAN, "metadata:\n  paths: src"), "F11", "warning")

    def test_f12_nobody_can_invoke_the_skill(self):
        self.only(self.skill(*CLEAN, "disable-model-invocation: true", "user-invocable: false"), "F12")

    def test_f13_a_comment_cuts_a_plain_value(self):
        self.only(self.skill("name: demo", "description: Before #after"), "F13", "warning")


class NameAndDescription(Case):
    def test_n1_portable_requires_a_name(self):
        root = self.skill("description: Does a thing.")
        self.assertEqual(self.found(root), [])
        self.only(root, "N1", portable=True)

    def test_n2_name_form(self):
        for name in ("Demo", "-demo", "demo-", "de--mo", "my_skill", "a" * 65):
            with self.subTest(name=name[:10]):
                self.only(self.skill(f"name: {name}", "description: x", name=name), "N2")
        self.assertEqual(self.found(self.skill("name: " + "a" * 64, "description: x", name="a" * 64)), [])

    def test_n3_name_matches_the_folder(self):
        problem = self.only(self.skill("name: other", "description: x"), "N3")
        self.assertEqual(problem.line, 2)

    def test_n4_reserved_names(self):
        for folder, name in (("synced", "synced"), ("Synced", None), ("anthropic-skills", "anthropic-skills")):
            with self.subTest(folder=folder):
                lines = ([f"name: {name}"] if name else []) + ["description: x"]
                self.assertIn(("N4", "error"), self.rules(self.skill(*lines, name=folder)))

    def test_n5_a_description_is_required(self):
        for lines in (("name: demo",), ("name: demo", "description:"), ("name: demo", 'description: "  "')):
            with self.subTest(lines=lines):
                self.only(self.skill(*lines), "N5")

    def test_n6_description_length(self):
        self.only(self.skill("name: demo", "description: " + "x" * 1025), "N6")
        self.assertEqual(self.found(self.skill("name: demo", "description: " + "x" * 1024)), [])

    def test_n7_no_angle_brackets(self):
        self.only(self.skill("name: demo", "description: Reads <files>."), "N7")

    def test_n8_reserved_words_in_the_name(self):
        root = self.skill("name: claude-helper", "description: x", name="claude-helper")
        self.only(root, "N8", "warning")
        self.only(root, "N8", portable=True)

    def test_n9_when_to_use_belongs_in_the_description(self):
        self.only(self.skill(*CLEAN, "when_to_use: When asked."), "N9", "warning")

    def test_n10_description_and_when_to_use_together(self):
        root = self.skill("name: demo", "description: " + "x" * 1000, "when_to_use: " + "y" * 600)
        self.assertEqual(sorted(self.rules(root)), [("N10", "error"), ("N9", "warning")])


class Command(Case):
    def run_audit(self, *args):
        return subprocess.run([sys.executable, "-B", str(SCRIPTS / "audit.py"), *map(str, args)],
                              capture_output=True, text=True)

    def test_an_error_fails_the_command(self):
        root = self.skill(*CLEAN, "tools: Read")
        result = self.run_audit(root)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn(f"{root / 'SKILL.md'}:4: [F6] unknown field `tools`", result.stdout)

    def test_a_warning_reports_without_failing(self):
        result = self.run_audit(self.skill("name: demo", "description: Before #after"))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("[F13] warning: ", result.stdout)

    def test_a_clean_skill_prints_its_count(self):
        result = self.run_audit(self.skill(*CLEAN))
        self.assertEqual((result.returncode, result.stdout.strip().splitlines()[-1]), (0, "1 skill audited, 0 errors, 0 warnings"))


if __name__ == "__main__":
    unittest.main()
