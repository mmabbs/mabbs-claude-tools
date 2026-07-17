# Skill Sanitizer

Takes a personal Claude Code skill and produces a copy ready for public release. The live skill is never touched — all transformations happen on a staging copy, gated by a final sweep before anything reaches the repo.

1. **Canonicalize** — finds every copy of the skill (live, staging, exports), diffs them, and merges into one canonical version.
2. **Assess** — reads every file and presents findings in three buckets: sanitization issues, polish items, and what needs writing. No edits happen until you've seen the full picture.
3. **Blockers and advisories** — reports objective defects (broken references, missing scripts) separately from subjective observations. Blockers gate the repo move; advisories are stated once and dropped.
4. **Copy to staging** — creates the working copy in your staging directory.
5. **Mechanical pass** — applies uniform transformations (strip vault metadata, replace personal names and paths, neutralize secrets, bundle referenced agents) without confirmation.
6. **Judgment pass** — presents keep/remove decisions that need human input: regional identity vs. personal interest, coupling strategy, positioning claims.
7. **Docs and gate** — writes the public README, runs a final grep sweep for names/paths/secrets, and only moves the skill to the repo when the sweep is clean and no blockers remain.
8. **Handoff** — offers an optional validation run via [skill-critic](../skill-critic/) and a commit.

## Sample output

After a run, the staging directory contains a sanitized skill folder:

```
skills-for-github-staging/daily-brief/
├── SKILL.md              # Clean frontmatter, no personal paths
├── README.md             # Public README with requirements table
├── references/
│   └── source-config.md  # API keys replaced with placeholders
├── scripts/
│   └── fetch_news.py     # Uses ${CLAUDE_SKILL_DIR}, not absolute paths
└── agents/
    └── daily-brief--summarizer.md  # Bundled agent definition
```

The mechanical pass report lists every change by file. The judgment pass presents each decision with a recommendation before applying.

## Requirements

| Component | Required? | Without it |
|-----------|-----------|------------|
| Claude Code | Required | The skill runs inside Claude Code sessions |
| A staging directory | Required | Nowhere to write the sanitized copy — configure in `references/repo-conventions.md` |
| A local git repo for publishing | Required | No destination for the final repo move — configure in `references/repo-conventions.md` |
| [skill-critic](../skill-critic/) | Optional | The Stage 8 validation offer is skipped; sanitization itself is unaffected |

## Installation

```bash
# Clone the repo
git clone https://github.com/your-username/your-skills-repo.git

# Copy the skill folder to your Claude Code skills directory
cp -r your-skills-repo/skills/skill-sanitizer ~/.claude/skills/skill-sanitizer
```

## Configuration

Before first use, edit `references/repo-conventions.md` and replace the placeholder paths with your own:

| Placeholder | Replace with |
|-------------|-------------|
| `/path/to/your/staging/directory/` | Your staging directory for sanitized copies |
| `/path/to/your/local/skills-repo/` | Your local git repo for published skills |
| `https://github.com/your-username/your-skills-repo/` | Your GitHub repo URL |

Also update the final sweep grep pattern in the same file — add your username, vault names, and any personal identifiers you want the sweep to catch.

## Bundled files

| File | Purpose |
|------|---------|
| `SKILL.md` | The skill instructions Claude follows during a run |
| `references/repo-conventions.md` | Your staging/repo paths, triage criteria, gate checklist — configure before first use |
| `references/mechanical-pass.md` | The uniform transformations applied without confirmation |
| `references/judgment-pass.md` | Keep/remove decisions that need human input |
| `references/readme-template.md` | Structure and writing rules for the public README the skill generates |

## Changelog

### 2026-07-17

- Initial public release.
