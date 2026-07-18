# cc-health

A Claude Code plugin that audits your Claude Code infrastructure across 7 domains — conversations, config, assets (skills/agents/plugins), memory, version compatibility, debris, and temp files. Report-first: scanners are read-only, fixes happen only after you confirm.

## What it does

1. You invoke `/cc-health <domain>` (or `/cc-health full` to run everything).
2. A Python scanner reads the relevant slice of `~/.claude/` and outputs structured JSON findings.
3. Claude formats the findings as a severity-grouped report (errors → warnings → info).
4. You review the report and optionally ask Claude to fix actionable items.

The `version` domain works differently — it slices the CC changelog between your last-seen version and the current one, classifies entries for breaking changes using a dedicated agent, and checks whether any affect your config.

A SessionStart hook nudges you when Claude Code updates, so you know to run `/cc-health version` before a breaking change surprises you.

## Sample output

```
## cc-health Report — config

**Summary:** 0 errors, 2 warnings, 1 info

### Warnings
| Check                  | Message                                                      | Suggested Action                     |
|------------------------|--------------------------------------------------------------|--------------------------------------|
| orphaned-project-entry | Project entry points to non-existent directory: -Users-jdoe… | Remove the entry from .claude.json   |
| mcp-scope-mismatch     | MCP server 'obsidian' local-scoped to non-existent dir       | Remove or re-scope to 'user'         |

### Info
| Check                | Message                                              | Suggested Action                         |
|----------------------|------------------------------------------------------|------------------------------------------|
| duplicate-permission | Permission 'Bash(git:*)' in both settings files      | Remove from one (settings.local wins)    |
```

## Domains

| Domain   | Scanner script        | What it checks                                            |
|----------|-----------------------|-----------------------------------------------------------|
| `chats`  | `cc-health-chats.py`  | Conversations — scan, usage, clean, orphans               |
| `config` | `cc-health-config.py` | Config files, scoping, permissions, MCP                   |
| `assets` | `cc-health-assets.py` | Skills, agents, plugins, trigger clashes (TF-IDF)         |
| `memory` | `cc-health-memory.py` | MEMORY.md entries, stale paths, dated entries              |
| `version`| (orchestrated inline) | Changelog classification, breaking-change detection       |
| `debris` | `cc-health-debris.py` | Orphaned agents, TODO/FIXME markers                       |
| `temp`   | `cc-health-temp.py`   | Scratch files, artifact droppings, stale context files    |
| `full`   | (all of the above)    | Run every domain sequentially                             |

## Requirements

| Component               | Required? | Without it                                                        |
|--------------------------|-----------|-------------------------------------------------------------------|
| Claude Code              | Required  | Plugin won't load                                                 |
| Python 3.10+             | Required  | Scanners won't run (stdlib only — no pip dependencies)            |
| Plugin support (v2.1+)   | Required  | Plugin system must be available for hook registration             |
| Opus model access        | Optional  | `version` domain's changelog classifier requires Opus; other domains work on any model |

## Installation

1. Clone or copy this folder into your local plugins directory:

   ```bash
   cp -r cc-health ~/.claude/plugins/local/cc-health
   ```

2. Create the marketplace wrapper (required for local plugin discovery):

   ```bash
   mkdir -p ~/.claude/plugins/local/cc-health/.claude-plugin
   # plugin.json is already included — verify it exists:
   cat ~/.claude/plugins/local/cc-health/.claude-plugin/plugin.json
   ```

3. Register the marketplace and install:

   ```bash
   claude plugin marketplace add ~/.claude/plugins/local/cc-health
   claude plugin install cc-health
   ```

4. Enable the plugin:

   ```bash
   claude plugin enable cc-health
   ```

5. Restart Claude Code. The SessionStart hook will initialize on first run.

## Usage

```
/cc-health config                          # Run config domain
/cc-health assets                          # Check skills, agents, plugins
/cc-health assets --deep                   # Include description-drift check (spawns agents)
/cc-health assets --clash-threshold 0.25   # Lower trigger-clash sensitivity
/cc-health chats scan --empty-only         # Find empty sessions
/cc-health chats clean --confirm           # Delete matched sessions
/cc-health chats usage                     # Disk usage by project
/cc-health chats orphans                   # Find conversations for deleted projects
/cc-health version                         # Check for breaking changes since last run
/cc-health full                            # Run all domains
```

## Bundled files

| Path                                    | What it is                                                |
|-----------------------------------------|-----------------------------------------------------------|
| `skills/cc-health/SKILL.md`             | Main skill instructions — Claude's orchestration guide    |
| `skills/cc-health/references/`          | Reference docs for path encoding and config load semantics|
| `agents/changelog-classifier/AGENT.md`  | Agent definition for version-domain changelog analysis    |
| `scripts/cc-health-*.py`               | Domain scanner scripts (one per domain)                   |
| `scripts/lib/`                          | Shared Python modules (schema, frontmatter, TF-IDF)      |
| `scripts/version-detect.sh`            | SessionStart hook script — detects CC version changes     |
| `hooks/hooks.json`                      | Hook registration for the SessionStart nudge              |
| `state/.cc-health-state.json`           | Persistent state (last-seen version, trigger-clash baseline) |
| `tests/`                                | pytest test suite for all scanners                        |
| `.claude-plugin/plugin.json`            | Plugin manifest                                           |

## Changelog

### 2026-07-18

- Initial public release as cc-health v2.0.0 (successor to cc-audit).
- 7 audit domains: chats, config, assets, memory, version, debris, temp.
- TF-IDF trigger-clash detection with delta reporting and routing-override awareness.
- DFS path resolver for lossy hyphen-encoded project paths.
- Changelog classifier agent for breaking-change detection.
- SessionStart hook for version-change nudges.
- Full pytest suite covering all scanner domains.
