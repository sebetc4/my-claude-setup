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

    def test_f6_names_the_skill_field_for_an_agent_field(self):
        problem = self.only(self.skill(*CLEAN, "tools: Read"), "F6")
        self.assertIn("did you mean `allowed-tools`", problem.message)

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


class Size(Case):
    def write(self, root, relative, text):
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def test_z1_body_tokens(self):
        self.only(self.skill(*CLEAN, body="x" * 20004 + "\n"), "Z1")
        self.assertEqual(self.found(self.skill(*CLEAN, body="x" * 19999 + "\n")), [])

    def test_z2_skill_md_lines(self):
        self.only(self.skill(*CLEAN, body="x\n" * 496), "Z2", "warning")
        self.assertEqual(self.found(self.skill(*CLEAN, body="x\n" * 495)), [])

    def test_z3_a_long_reference_has_contents(self):
        root = self.skill(*CLEAN, body="See `references/big.md`.\n")
        big = self.write(root, "references/big.md", "# Big\n" + "line\n" * 299)
        problem = self.only(root, "Z3")
        self.assertEqual(problem.path, big)
        self.write(root, "references/big.md", "# Big\n\n## Contents\n" + "line\n" * 299)
        self.assertEqual(self.found(root), [])
        self.write(root, "references/big.md", "# Big\n" + "line\n" * 298)
        self.assertEqual(self.found(root), [])

    def test_z4_references_one_level_deep(self):
        root = self.skill(*CLEAN, body="See `references/a.md`.\n")
        self.write(root, "references/a.md", "Then `references/b.md`.\n")
        b = self.write(root, "references/b.md", "Detail.\n")
        problem = self.only(root, "Z4", "warning")
        self.assertEqual((problem.path, problem.message), (b, "reached only through `references/a.md`: cite it from `SKILL.md`"))


class Resources(Case):
    write = Size.write

    def test_r1_a_cited_file_exists(self):
        for body in ("See `references/missing.md`.\n", "See [the guide](references/missing.md).\n"):
            with self.subTest(body=body):
                problem = self.only(self.skill(*CLEAN, body="Intro.\n" + body), "R1")
                self.assertEqual((problem.line, problem.message), (7, "cites `references/missing.md`, which does not exist"))

    def test_r1_ignores_urls_and_anchors(self):
        root = self.skill(*CLEAN, body="See https://example.org/scripts/run.py and [above](#usage).\n")
        self.assertEqual(self.found(root), [])

    def test_r2_a_citation_leaving_the_skill(self):
        self.only(self.skill(*CLEAN, body="See `../other/references/x.md`.\n"), "R2", "warning")

    def test_r3_every_file_is_reached(self):
        root = self.skill(*CLEAN)
        orphan = self.write(root, "references/orphan.md", "Unused.\n")
        notes = self.write(root, "notes.md", "Unused.\n")
        self.assertEqual(sorted((p.rule, p.path) for p in self.found(root)), [("R3", notes), ("R3", orphan)])

    def test_r3_follows_links_imports_modules_and_the_license(self):
        root = self.skill(*CLEAN, "license: LICENSE.txt",
                          body="Run `scripts/main.py`, or `python -m scripts.tool`. See [notes](notes.md).\n")
        self.write(root, "LICENSE.txt", "Terms.\n")
        self.write(root, "notes.md", "Notes.\n")
        self.write(root, "scripts/main.py", "#!/usr/bin/env python3\nimport helper\nfrom lib import thing\n")
        self.write(root, "scripts/helper.py", "X = 1\n")
        self.write(root, "scripts/lib.py", "thing = 1\n")
        self.write(root, "scripts/tool.py", "Y = 1\n")
        self.write(root, "evals/evals.json", "{}\n")
        self.write(root, "scripts/__pycache__/helper.cpython-314.pyc", "")
        self.assertEqual([p.rule for p in self.found(root) if p.rule.startswith("R")], [])

    def test_r3_counts_any_path_of_the_skill_a_file_names(self):
        root = self.skill(*CLEAN, "license: Complete terms in LICENSE.txt",
                          body="Read `agents/grader.md` and `visual-companion.md`; run `python -m scripts.run_loop`.\n"
                               "Dimensions in `prompts/`: `skill-timeline.md`.\n")
        for relative in ("LICENSE.txt", "agents/grader.md", "visual-companion.md", "prompts/skill-timeline.md"):
            self.write(root, relative, "Text.\n")
        self.write(root, "scripts/__init__.py", "")
        self.write(root, "scripts/run_loop.py", "from scripts.utils import a\nfrom .report import b\n"
                                                 "VIEW = Path(__file__).parent / 'viewer.html'\n")
        self.write(root, "scripts/utils.py", "a = 1\n")
        self.write(root, "scripts/report.py", "b = 1\n")
        self.write(root, "scripts/viewer.html", "<html></html>\n")
        self.assertEqual([(p.rule, p.path.name) for p in self.found(root) if p.rule.startswith("R")], [])

    def test_r1_skips_example_links_and_placeholders(self):
        body = "See [topics](topics/<subject>.md).\n\n```markdown\nSee [forms](FORMS.md).\n```\n"
        self.assertEqual(self.found(self.skill(*CLEAN, body=body)), [])

    def test_r3_reads_prefixed_and_extensionless_paths(self):
        root = self.skill(*CLEAN, body="Run `${CLAUDE_SKILL_DIR}/scripts/render.py`, then `scripts/task-start`.\n"
                                       "Read `skills/demo/visual.md`.\n")
        for relative in ("scripts/render.py", "scripts/task-start", "visual.md"):
            self.write(root, relative, "x\n")
        self.assertEqual([(p.rule, p.path.name) for p in self.found(root) if p.rule.startswith("R")], [])

    def test_r3_a_cited_folder_reaches_its_files(self):
        root = self.skill(*CLEAN, body="The seeds are in `assets/templates/`, one `index.md` per preset.\n")
        self.write(root, "assets/templates/letter/index.md", "x\n")
        self.write(root, "assets/templates/report/index.md", "x\n")
        self.assertEqual([(p.rule, p.path.name) for p in self.found(root) if p.rule.startswith("R")], [])

    def test_r4_forward_slashes(self):
        root = self.skill(*CLEAN, body="See `references\\guide.md`, then `references/guide.md`.\n")
        self.write(root, "references/guide.md", "Guide.\n")
        self.only(root, "R4", "warning")


class Execution(Case):
    write = Size.write

    def script(self, root, relative, text, executable=True):
        path = self.write(root, relative, text)
        path.chmod(0o755 if executable else 0o644)
        return path

    def test_x1_an_injected_command_that_can_fail(self):
        for body in ("Status: !`git status`\n", "```!\nnode --version\n```\n"):
            with self.subTest(body=body):
                self.only(self.skill(*CLEAN, body=body), "X1", "warning")
        for body in ("Status: !`git status || true`\n", "Set KEY=!`cmd` here.\n"):
            with self.subTest(body=body):
                self.assertEqual(self.found(self.skill(*CLEAN, body=body)), [])

    def test_x2_scripts_are_executables_or_imported_modules(self):
        root = self.skill(*CLEAN, body="Run `scripts/run.py`.\n")
        run = self.script(root, "scripts/run.py", "#!/usr/bin/env python3\nprint(1)\n", executable=False)
        self.assertEqual(self.only(root, "X2").path, run)
        run.chmod(0o755)
        self.assertEqual(self.found(root), [])
        lib = self.script(root, "scripts/lib.py", "X = 1\n", executable=False)
        self.assertIn(("X2", lib), [(p.rule, p.path) for p in self.found(root)])
        run.write_text("#!/usr/bin/env python3\nimport lib\n", encoding="utf-8")
        self.assertEqual(self.found(root), [])

    def test_x2_a_package_marker_is_imported_with_its_package(self):
        root = self.skill(*CLEAN, body="Run `python -m scripts.run`.\n")
        self.script(root, "scripts/__init__.py", "", executable=False)
        self.script(root, "scripts/run.py", "from scripts.helper import x\n", executable=False)
        self.script(root, "scripts/helper.py", "x = 1\n", executable=False)
        self.assertEqual([(p.rule, p.path.name) for p in self.found(root)], [("X2", "run.py")])

    def test_x3_a_script_run_through_an_interpreter(self):
        root = self.skill(*CLEAN, body="Run `python3 scripts/run.py`.\n")
        self.script(root, "scripts/run.py", "#!/usr/bin/env python3\n")
        self.only(root, "X3", "warning")

    def test_x4_an_allowed_tools_rule_matching_no_command(self):
        self.only(self.skill(*CLEAN, "allowed-tools: Bash(gh *) Read", body="Read the file.\n"), "X4", "warning")
        self.assertEqual(self.found(self.skill(*CLEAN, "allowed-tools: Bash(gh *) Read", body="Run `gh pr view`.\n")), [])

    def test_x5_an_at_reference(self):
        root = self.skill(*CLEAN, body="See @references/guide.md for the rest.\n")
        self.write(root, "references/guide.md", "Guide.\n")
        self.only(root, "X5", "warning")

    def test_x6_ultrathink(self):
        self.only(self.skill(*CLEAN, body="Think it through: ultrathink.\n"), "X6", "warning")

    def test_x7_a_dollar_the_harness_would_replace(self):
        for lines, body in ((CLEAN, "It costs $1.00.\n"), (CLEAN, "Use $ARGUMENTS.\n")):
            with self.subTest(body=body):
                self.only(self.skill(*lines, body=body), "X7", "warning")
        for lines, body in ((CLEAN, "It costs \\$1.00.\n"), (CLEAN + ("arguments: [issue]",), "Fix $issue, then $ARGUMENTS.\n")):
            with self.subTest(body=body):
                self.assertEqual(self.found(self.skill(*lines, body=body)), [])


class Conventions(Case):
    write = Size.write

    def repo(self, skills_table, top='language = "english"\n', gitignore=None):
        repo = self.tmp / "repo"
        repo.mkdir()
        subprocess.run(["git", "init", "-q", str(repo)], check=True)
        (repo / ".agent-conventions.toml").write_text(top + "\n[skills]\n" + skills_table, encoding="utf-8")
        if gitignore is not None:
            (repo / ".gitignore").write_text(gitignore, encoding="utf-8")
        return repo

    def skill_in(self, repo, where, *lines, body="Body.\n"):
        root = repo / where
        root.mkdir(parents=True)
        (root / "SKILL.md").write_text("---\n" + "".join(l + "\n" for l in lines) + "---\n\n" + body, encoding="utf-8")
        return root

    def conv(self, root, **options):
        return [(p.rule, p.severity) for p in self.found(root, **options) if p.rule.startswith("C")]

    def test_no_conventions_no_convention_rule(self):
        repo = self.tmp / "bare"
        (repo / ".git").mkdir(parents=True)
        root = self.skill_in(repo, "anywhere/demo", *CLEAN, body="Ask Claude to read it: 50 %.\n")
        self.assertEqual(self.conv(root), [])

    def test_c1_the_skill_sits_in_a_skill_folder(self):
        repo = self.repo('dirs = ["skills"]\n')
        self.assertEqual(self.conv(self.skill_in(repo, "skills/demo", *CLEAN)), [])
        self.assertEqual(self.conv(self.skill_in(repo, "other/demo", *CLEAN)), [("C1", "error")])

    def test_c1_leaves_out_the_eval_workspace(self):
        repo = self.repo('dirs = ["skills"]\nworkspace = ".eval-runs"\n', gitignore=".eval-runs/\n")
        run = self.skill_in(repo, ".eval-runs/skills/demo/baseline/release/releasing-domains", *CLEAN)
        self.assertEqual(self.conv(run), [])
        self.assertEqual(self.conv(self.skill_in(repo, "eval-runs/demo", *CLEAN)), [("C1", "error")])

    def test_c2_evaluations_sit_in_the_evals_folder(self):
        repo = self.repo('dirs = ["skills"]\nevals = "evals"\n')
        root = self.skill_in(repo, "skills/demo", *CLEAN)
        self.write(root, "tests/test_demo.py", "x = 1\n")
        self.write(root, "evals/evals.json", "{}\n")
        self.assertEqual(self.conv(root), [("C2", "error")])

    def test_c3_the_declared_language(self):
        repo = self.repo('dirs = ["skills"]\n')
        root = self.skill_in(repo, "skills/demo", *CLEAN, body="Lire le fichier.\nIt is 50 % done.\n")
        self.assertEqual(self.conv(root), [("C3", "error"), ("C3", "error")])

    def test_c4_the_files_address_the_agent(self):
        repo = self.repo('dirs = ["skills"]\naddress = "agent"\n')
        self.assertEqual(self.conv(self.skill_in(repo, "skills/demo", *CLEAN, body="Ask Claude to read it.\n")),
                         [("C4", "error")])
        self.assertEqual(self.conv(self.skill_in(repo, "skills/other", "name: other", "description: x",
                                                 body="Claude Code runs it; any agent can.\n")), [])

    def test_c5_excluded_features(self):
        repo = self.repo('dirs = ["skills"]\nexclude = ["allowed-tools", "dynamic-context", "substitutions"]\n')
        for where, lines, body in (("skills/a", ("name: a", "description: x", "allowed-tools: Read"), "Body.\n"),
                                   ("skills/b", ("name: b", "description: x"), "Now: !`date || true`\n"),
                                   ("skills/c", ("name: c", "description: x"), "Run ${CLAUDE_SKILL_DIR}/x.\n")):
            with self.subTest(where=where):
                self.assertEqual(self.conv(self.skill_in(repo, where, *lines, body=body)), [("C5", "error")])

    def test_c6_the_workspace_is_ignored_by_git(self):
        repo = self.repo('dirs = ["skills"]\nworkspace = ".eval-runs"\n')
        self.assertEqual(self.conv(self.skill_in(repo, "skills/demo", *CLEAN)), [("C6", "error")])
        (repo / ".gitignore").write_text("/.eval-runs/\n", encoding="utf-8")
        self.assertEqual(self.conv(self.skill_in(repo, "skills/other", "name: other", "description: x")), [])

    def test_c7_the_repository_checks_under_checks_only(self):
        repo = self.repo('dirs = ["skills"]\n', top='language = "english"\nchecks = ["false"]\n')
        root = self.skill_in(repo, "skills/demo", *CLEAN)
        self.assertEqual(self.conv(root), [])
        self.assertEqual(self.conv(root, checks=True), [("C7", "error")])


class Text(Case):
    def test_t1_compatibility_wording(self):
        for body in ("Keep the legacy format.\n", "This field is deprecated.\n", "Stay backward compatible.\n"):
            with self.subTest(body=body):
                self.only(self.skill(*CLEAN, body=body), "T1", "warning")

    def test_t1_lets_an_edit_name_its_baseline(self):
        self.assertEqual(self.found(self.skill(*CLEAN, body="Run the old version, then the previous version.\n")), [])


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
