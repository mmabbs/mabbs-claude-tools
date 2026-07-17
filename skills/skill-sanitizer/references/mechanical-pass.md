# Mechanical Pass

Apply every item to the staging copy. No confirmation needed. Report changes afterward, grouped by file.

## 1. Delete workspace artifacts

- **Remove `<!-- @format -->` comments, `__pycache__/`, `*.pyc`, `.DS_Store`.** They signal "copied from a personal project, not published."

## 2. Strip vault metadata from frontmatter

- **Keep only Claude Code-native fields:** `name`, `description`, `argument-hint`, `effort`, `compatibility`. Strip vault fields: `title`, `aliases`, `uid`, `created`, `modified`, `tags`, `domain`, `note-type`, `categories`, `cssclasses`, `project`, and any wikilink-valued field.
- **Never strip `effort` or `argument-hint` as "personal config."** They are standard fields that control execution and autocomplete. Stripping them breaks the skill for adopters.
- **Exception: strip null hints like `argument-hint: (no arguments)`.** A hint with no content is autocomplete noise. Hints listing real modes (`ask|add|list`) stay.
- **Never add fields the original lacks.** Preserve what exists — a missing `effort` or `argument-hint` stays missing. Adding one is authoring, not sanitizing.

## 3. Replace personal names

- **The author's name becomes "the user" throughout.** "Alice's Claude Code setup" becomes "a Claude Code setup." Check prose, examples, comments, and prompts inside agent briefs.

## 4. Fix paths

- **Bundled script invocations use `${CLAUDE_SKILL_DIR}/scripts/<name>`.** Never an absolute path — and never a bare relative path like `scripts/foo.py` either: relative paths resolve against Claude's current working directory, which is almost never the skill folder, so the invocation breaks in every real session. The variable works from anywhere.
- **Markdown links stay relative.** `[references/x.md](references/x.md)` resolves natively — do not rewrite links to use the variable. It exists for bash injections only.
- **Output locations default to the current working directory.** Replace every hardcoded output path with "save to the current working directory unless the user specifies a location."
- **Shell scripts derive co-located paths:** `SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"`, then `"$SCRIPT_DIR/<file>"`.
- **Hook scripts derive paths from the hook's JSON payload when it carries them** (e.g., `transcript_path`). Only fall back to a `# Configure:` constant when the payload lacks the data.
- **User-specific constants in Python get `# Configure:` comments** stating what to change and why.

## 5. Neutralize secrets

- **Replace API keys, calendar IDs, account names, and tokens with placeholders** plus a one-line configuration instruction at the point of use.
- **Report secrets in their own section, above everything else.** A leaked path embarrasses; a leaked key compromises.

## 6. Fix identity strings

- **Replace borrowed or fake identities in User-Agent and contact fields** with a generic tool identifier, e.g., `SkillName/1.0 (purpose)`. Never leave a real organization's name or email in place.

## 7. Inline personal-config citations

- **Replace "per <author's config file>" with the reasoning itself.** "Per agent-model-selection.md, extraction runs on Sonnet" becomes "Extraction runs on Sonnet — fast, cheap, reliable for structured operations." The rule stays hard; only the authority changes.

## 8. Genericize vault jargon

- **Replace Obsidian-specific terms when the mechanism is generic.** "Wikilinks to all notes" becomes "links to all notes." Leave the term only when the skill genuinely requires Obsidian.

## 9. Replace personal example data

- **Swap personal project names for obviously-generic ones** (Alpha, Beta, Web Platform). Never leave blanks — structure must stay readable.

## 10. Bundle referenced agents

- **If the skill spawns named agent types** (`subagent_type: "skill-name--helper"`), copy those agent definition files into an `agents/` folder in the staging copy. The README's install steps must tell users to copy them to `~/.claude/agents/` — without the files, every spawn fails in an adopter's environment.
- **If no definition exists anywhere** (`~/.claude/agents/`, the skill folder, the staging copy), do not write one. A fabricated agent is invented behavior shipped under the author's name. Flag it as a blocker — the skill references an agent that doesn't exist — and ask the user. In non-interactive runs, record the blocker in the report; the repo move stays blocked either way.
