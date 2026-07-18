# Load Semantics Reference

Rules that govern how Claude Code discovers and loads configuration. The config scanner uses these to detect mis-scoped config.

## Inheritance Rules

| Asset | Inherits up-tree? | Notes |
|-------|-------------------|-------|
| CLAUDE.md | Yes (ancestors at launch) | Nested subdir CLAUDE.md loads on-demand when files in that subtree are read |
| settings.json | No | Loads ONLY from the launch-root — not ancestors |
| agents/ | No | Only launch-root `.claude/agents/` plus global `~/.claude/agents/` |
| .claude/rules/ | Undocumented | Don't assume ancestor rules load in subfolder launches |
| MCP (local scope) | No | Keyed to the exact launch directory path |
| skills/ | Partial | launch-root + ancestors up to repo root + global + plugins |

## Implications for Auditing

1. A `settings.json` placed in a subdirectory of a project will NOT load when the user launches from the project root. Only the launch-root's settings.json loads.

2. An MCP server local-scoped to `/Users/jdoe/projects/my-project/` will NOT connect when launching from `/Users/jdoe/projects/my-project/packages/api/`.

3. CLAUDE.md files in nested subdirectories are loaded on-demand — they're not guaranteed to be in context after `/compact`.

4. A permission in `settings.json` at the vault root won't apply when launching from a project subdirectory (settings don't inherit).

## Conflict Resolution

Multiple CLAUDE.md files are concatenated, not overridden. On direct conflict, Claude may pick one arbitrarily — there is no hard precedence ladder. The launch-root's advantage is reliability (always loaded), not rank.
