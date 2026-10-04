"""Tests for the frontmatter reader: a strict subset of YAML, standard library only."""

import importlib.util
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "frontmatter.py"
_spec = importlib.util.spec_from_file_location("frontmatter", SCRIPT)
frontmatter = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(frontmatter)


def fm(*lines, body="Body.\n"):
    return "---\n" + "".join(line + "\n" for line in lines) + "---\n\n" + body


def fields(*lines):
    result = frontmatter.parse(fm(*lines))
    assert not result.problems and not result.outside, (result.problems, result.outside)
    return result.fields


def codes(text):
    return [code for _, code, _ in frontmatter.parse(text).problems]


class Values(unittest.TestCase):
    def test_plain_values_are_strings(self):
        self.assertEqual(fields("name: my-skill", "description: Does a thing."),
                         {"name": "my-skill", "description": "Does a thing."})

    def test_plain_scalars_are_typed_by_the_core_schema(self):
        self.assertEqual(fields("a: 123", "b: true", "c: False", "d: ~", "e: null", "f: 1.5", "g:", "h: yes"),
                         {"a": 123, "b": True, "c": False, "d": None, "e": None, "f": 1.5, "g": None, "h": "yes"})

    def test_quoted_values_stay_strings(self):
        self.assertEqual(fields("a: \"123\"", "b: 'true'", "c: 'it''s'", 'd: "tab\\tquote\\" é"'),
                         {"a": "123", "b": "true", "c": "it's", "d": 'tab\tquote" é'})

    def test_a_plain_value_may_hold_a_colon_without_a_space(self):
        self.assertEqual(fields("a: see http://example.org/x"), {"a": "see http://example.org/x"})

    def test_a_plain_value_continued_on_more_indented_lines_is_folded(self):
        self.assertEqual(fields("description: A plain value", "  continued here."),
                         {"description": "A plain value continued here."})

    def test_folded_and_literal_blocks(self):
        self.assertEqual(fields("a: >-", "  Folded over", "  two lines.", "b: |", "  Line one.", "  Line two."),
                         {"a": "Folded over two lines.", "b": "Line one.\nLine two.\n"})

    def test_flow_collections_of_scalars(self):
        self.assertEqual(fields("a: [Read, \"Grep\", 'Glob']", "b: {author: me, version: \"1.0\"}"),
                         {"a": ["Read", "Grep", "Glob"], "b": {"author": "me", "version": "1.0"}})

    def test_block_sequences_and_nested_mappings(self):
        self.assertEqual(
            fields("allowed-tools:", "- Read", "- Grep", "hooks:", "  PreToolUse:", "    - matcher: Bash",
                   "      hooks:", "        - type: command", "          command: ./check.sh"),
            {"allowed-tools": ["Read", "Grep"],
             "hooks": {"PreToolUse": [{"matcher": "Bash", "hooks": [{"type": "command", "command": "./check.sh"}]}]}})

    def test_comments_are_skipped(self):
        self.assertEqual(fields("# a comment", "name: x  # trailing"), {"name": "x"})

    def test_crlf_line_ends_and_a_byte_order_mark(self):
        text = "﻿---\r\nname: x\r\ndescription: y\r\n---\r\nBody.\r\n"
        self.assertEqual(frontmatter.parse(text).fields, {"name": "x", "description": "y"})

    def test_an_empty_frontmatter_is_an_empty_mapping(self):
        self.assertEqual(frontmatter.parse("---\n---\nBody.\n").fields, {})

    def test_the_line_of_each_key_and_where_the_body_starts(self):
        result = frontmatter.parse(fm("name: x", "description: >-", "  y"))
        self.assertEqual(result.lines, {"name": 2, "description": 3})
        self.assertEqual(result.body_line, 6)

    def test_a_plain_value_cut_by_a_comment_is_noted(self):
        result = frontmatter.parse(fm("description: Before #after"))
        self.assertEqual(result.fields, {"description": "Before"})
        self.assertEqual(result.cut, [(2, "description")])


class Problems(unittest.TestCase):
    def test_no_opening_line(self):
        self.assertEqual(codes("\n---\nname: x\n---\n"), ["no-opening"])
        self.assertIsNone(frontmatter.parse("Just text.\n").fields)

    def test_never_closed(self):
        self.assertEqual(codes("---\nname: x\n\nBody.\n"), ["no-closing"])

    def test_three_dots_do_not_close(self):
        self.assertEqual(codes("---\nname: x\n...\nBody.\n"), ["no-closing"])

    def test_not_a_mapping(self):
        self.assertEqual(codes(fm("- name: x")), ["not-mapping"])

    def test_yaml_errors(self):
        for line in ("description: It runs after: always.", "description: @file first", "description: `code` first",
                     "description: \"never closed"):
            with self.subTest(line=line):
                self.assertEqual(codes(fm("name: x", line)), ["yaml"])

    def test_a_tab_in_the_indentation(self):
        self.assertEqual(codes(fm("metadata:", "\tauthor: me")), ["yaml"])

    def test_a_duplicated_key(self):
        result = frontmatter.parse(fm("name: x", "name: y"))
        self.assertEqual([(line, code) for line, code, _ in result.problems], [(3, "yaml")])
        self.assertIn("duplicate", result.problems[0][2])

    def test_a_problem_names_its_line(self):
        self.assertEqual(frontmatter.parse(fm("name: x", "description: a: b")).problems[0][0], 3)


class Outside(unittest.TestCase):
    def test_valid_yaml_the_subset_does_not_read(self):
        for lines in (("description: &d Text",), ("description: *d",), ("description: !!str Text",),
                      ("\"description\": Text",), ("description: \"two", "  lines\""), ("a: [x, [y]]",)):
            with self.subTest(lines=lines):
                result = frontmatter.parse(fm(*lines))
                self.assertEqual(result.problems, [])
                self.assertEqual(len(result.outside), 1)


if __name__ == "__main__":
    unittest.main()
