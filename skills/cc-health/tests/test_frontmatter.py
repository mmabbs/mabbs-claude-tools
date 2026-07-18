"""Tests for SKILL.md frontmatter parser."""

import sys
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from lib.frontmatter import parse_skill_frontmatter


def test_single_line_description():
    text = textwrap.dedent("""\
        ---
        name: my-skill
        description: A simple skill that does one thing.
        ---
        Body content here.
    """)
    result = parse_skill_frontmatter(text)
    assert result["name"] == "my-skill"
    assert result["description"] == "A simple skill that does one thing."
    assert result["whenToUse"] is None


def test_folded_scalar_description():
    text = textwrap.dedent("""\
        ---
        name: router
        description: >
          Routes any game-development request to the right
          specialized skill. Use to make a game or to decide
          which skill applies.
        license: Apache-2.0
        ---
        Body content.
    """)
    result = parse_skill_frontmatter(text)
    assert result["name"] == "router"
    assert "Routes any game-development" in result["description"]
    assert "which skill applies." in result["description"]
    # Folded scalar joins lines with spaces
    assert "\n" not in result["description"]


def test_literal_scalar_description():
    text = textwrap.dedent("""\
        ---
        name: my-skill
        description: |
          Line one.
          Line two.
          Line three.
        ---
        Body.
    """)
    result = parse_skill_frontmatter(text)
    assert "Line one." in result["description"]
    assert "Line three." in result["description"]


def test_when_to_use_field():
    text = textwrap.dedent("""\
        ---
        name: my-skill
        description: Does something.
        whenToUse: When the user asks to do the thing.
        ---
        Body.
    """)
    result = parse_skill_frontmatter(text)
    assert result["whenToUse"] == "When the user asks to do the thing."


def test_quoted_description():
    text = textwrap.dedent("""\
        ---
        name: my-skill
        description: "A skill with 'quotes' inside."
        ---
        Body.
    """)
    result = parse_skill_frontmatter(text)
    assert result["description"] == "A skill with 'quotes' inside."


def test_no_frontmatter():
    text = "Just some markdown without frontmatter."
    result = parse_skill_frontmatter(text)
    assert result["name"] is None
    assert result["description"] is None


def test_empty_description():
    text = textwrap.dedent("""\
        ---
        name: my-skill
        description:
        ---
        Body.
    """)
    result = parse_skill_frontmatter(text)
    assert result["description"] is None


def test_other_fields_ignored():
    text = textwrap.dedent("""\
        ---
        name: my-skill
        description: Does something.
        license: MIT
        argument-hint: ask|list
        compatibility: v2.0+
        ---
        Body.
    """)
    result = parse_skill_frontmatter(text)
    assert result["name"] == "my-skill"
    assert result["description"] == "Does something."
    assert "license" not in result
