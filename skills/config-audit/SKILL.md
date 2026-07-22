---
name: config-audit
description: "Scan all Claude Code config layers — rules, skills, hooks, plugins, MCP, memory, CLAUDE.md, agents — and audit placement. Use when the user asks to audit their setup, reassess or consolidate config, or says something is in the wrong layer."
argument-hint: save <to/path>|project <name>
---

# Config Audit

Scan every Claude Code configuration layer and assess whether each piece of config is in the right place. This is a placement auditor, not an automation recommender. The question isn't "what automations are you missing?" but "is everything stored in the layer that best serves it?"

This skill is most valuable after a setup has accumulated organically — after enough sessions that things have drifted, duplicated, or landed in the wrong layer because it was convenient at the time.

## Arguments

`/config-audit` — full sweep across all projects, present findings in chat.

`/config-audit project <name>` — scan only the named project's configs (plus global, since global affects every project). Skips other projects' `.claude/`, memory, and CLAUDE.md files.

`/config-audit save <to/path>` — write findings to a timestamped note in the specified directory instead of chat.

Arguments compose: `/config-audit project web-platform save <to/path>` scans one project and saves the findings.

## Progress Communication

This skill runs multiple phases with parallel agents. The user must never sit in silence wondering what's happening. At each phase boundary, tell the user what's about to happen and what to expect:

- Before spawning scanners: "Launching 8 scanner agents in parallel (one per config type). This will take 1-2 minutes — I'll report back when they've all returned."
- As scanners return: Brief status updates as results come in, e.g., "6 of 8 scanners done."
- Before spawning the reasoning agent: "All inventories in. Launching the reasoning agent — this is the cross-layer analysis, expect ~1-2 minutes."
- When findings are ready: Present them.

If any agent takes unusually long or fails, say so immediately rather than waiting silently.

## Before Scanning

Verify the eight criteria docs exist in `references/` and note their full paths — do **not** read them into your own context. Each defines what earns its keep in a config layer, what disqualifies, and the boundary tests between adjacent types. Only the Phase 2 reasoning agent needs their content, and it reads them from disk itself; it cannot make sound recommendations without them — training data encodes obsolete boundary tests (e.g., skill-vs-agent used to hinge on context isolation; now skills can fork into subagents with pinned models).

Criteria docs:

| Doc | Covers |
|-----|--------|
| `references/criteria-rules.md` | Rules (`~/.claude/rules/`, `.claude/rules/`) |
| `references/criteria-skills.md` | Skills (`~/.claude/skills/`, `.claude/skills/`) |
| `references/criteria-hooks.md` | Hooks (configured in `settings.json`) |
| `references/criteria-plugins.md` | Plugins (`~/.claude/plugins/`) |
| `references/criteria-claude-md.md` | CLAUDE.md (global + project) |
| `references/criteria-mcp.md` | MCP servers (`.mcp.json`, `~/.claude.json`) |
| `references/criteria-agents.md` | Agent definitions (`~/.claude/agents/`, `.claude/agents/`) |
| `references/criteria-memory.md` | Memory files (`~/.claude/projects/<project>/memory/`) |

## Scope

By default, this skill scans global config plus **all** project directories. When `project <name>` is provided, scan only that project's configs plus global (since global affects every project).

Before Phase 1, build the list of project paths: if a CLAUDE.md in scope (project or global) lists project directories, read that list; otherwise ask the user which project directories to scan. Match `project <name>` against the directory names in that list (case-insensitive, partial match okay — e.g., `web-platform` matches "Web Platform" at `~/projects/web-platform/`). If ambiguous, ask. For each project in scope, check whether `<project-path>/.claude/` exists.

The scan covers:
- **Global config** — `~/.claude/` (rules, skills, agents, settings, CLAUDE.md) — always included
- **Project config** — `<project-path>/.claude/` (rules, skills, settings, CLAUDE.md) — all projects, or just the named one
- **Project memory** — `~/.claude/projects/<project-slug>/memory/` — all projects, or just the named one
- **Shared infrastructure** — plugins, MCP servers, hooks (which span all projects)

The `<project-slug>` is the project's absolute path with every `/` (and other separator characters like `.`) replaced by `-`: a project at `~/projects/my-app` has its memory at `~/.claude/projects/-Users-<username>-projects-my-app/memory/`. Use this mapping both to locate a named project's memory directory and to attribute discovered memory directories back to their projects.

The multi-project view is where the most valuable findings live — a global rule that should be project-scoped, a project rule that's duplicated across three projects and should be global, memory files that diverge across projects on the same topic.

## Phase 1: Scan

Spawn **one scanner agent per config type**, all in parallel (8 agents). Each scanner catalogs what exists in its layer **across all projects**. Scanners do not assess placement — they produce inventories. Reasoning happens in Phase 2.

Use **Sonnet** for scanners — they're doing extraction, not synthesis.

### What Each Scanner Reads

| Config Type | Paths |
|---|---|
| Rules | `~/.claude/rules/` + each project's `.claude/rules/` |
| Skills | `~/.claude/skills/` + each project's `.claude/skills/`. Read each SKILL.md frontmatter + first ~30 lines for purpose |
| Hooks | `~/.claude/settings.json` + `~/.claude/settings.local.json` + each project's `.claude/settings.json` and `.claude/settings.local.json`. Also grep `~/.claude/plugins/` for `hooks.json` — plugins register hooks that don't appear in settings files. For each plugin-registered hook, record whether the owning plugin is currently enabled — a disabled plugin's hooks never fire |
| Plugins | `~/.claude/plugins/` — check installed state (install records under `~/.claude/plugins/`), enabled state (`enabledPlugins` in settings files), and what each bundles |
| MCP Servers | `~/.claude.json` (check all local-scoped entries and their project paths) + each project's `.mcp.json` |
| Memory | `~/.claude/projects/*/memory/` for each project that has memory files — read MEMORY.md index + each memory file. Attribute each memory directory to its project via the path-encoded slug (see Scope) |
| CLAUDE.md | `~/.claude/CLAUDE.md` + each project's `.claude/CLAUDE.md`. Break down by section — each heading-level block is a separate inventory item. Tag each item with its project |
| Agents | `~/.claude/agents/` + each project's `.claude/agents/`. Read each definition's frontmatter + system prompt summary |

### Scanner Prompt

The scanner prompt template (including the inventory format scanners must follow) is in `references/scanner-prompt.md`. Read it and pass it to each scanner with `[TYPE]`, the paths from the table above (including any scanner-specific instructions in the table row), and the resolved `<workspace>` path filled in.

The **content character** field is what lets the reasoning agent spot misplacements. A memory file with "behavioral" character is probably a rule. An enforcement rule might be better as a hook or permission entry. A procedural CLAUDE.md section might be a skill.

### Workspace

Write inventories to `<scratchpad>/config-audit/`. `<scratchpad>` is the session scratchpad directory your environment provides; if none is defined, use a temp directory (e.g., `$TMPDIR/config-audit/`). This resolved path is the `<workspace>` used throughout — substitute the actual path when constructing agent prompts and commands. Create the directory if it doesn't exist. These are intermediate files — they don't persist beyond the session.

## Phase 2: Reason

After all scanners complete, spawn a **single reasoning agent** at **Opus** with **max effort**. This agent reads all 8 inventory files plus all 8 criteria docs, produces findings, and writes them to `<workspace>/findings.md`.

### Reasoning Agent Prompt

The reasoning agent prompt template is in `references/reasoning-prompt.md`. Read it and pass it to the agent with the inventory file paths, the criteria doc paths (the eight docs in the table above), and the resolved `<workspace>` path filled in. The template instructs the agent to write its full findings to `<workspace>/findings.md` and return only a one-line summary — relay that summary as the phase status update.

## Presenting Findings

The reasoning agent writes its findings to `<workspace>/findings.md`. Don't repeat them in chat — open the file with the platform's default opener so the user can read it directly: `open <workspace>/findings.md` on macOS, `xdg-open` on Linux (substitute the equivalent on other platforms).

After opening, give a one-line summary: finding counts by category and any `broken` items. Then ask which findings the user wants to act on. Nothing gets executed until they choose.

## Acting on Findings

When the user selects findings:

- **Relocations**: move the content to the new layer. Archive the original (don't delete — move to `~/.claude/archive/`). Show the user what changed.
- **Consolidations**: draft the bundle structure (plugin layout, combined skill, etc.) and present for review before writing.
- **Net-New**: draft the new config item and present for review before writing.

## Save Mode

When `save <dir>` is used:

1. Run the full audit
2. Write to `<dir>/config-audit-YYYY-MM-DD.md` (append counter if name exists)
3. Confirm in chat: file path + finding counts per category

### Note Format

```markdown
# Config Audit — YYYY-MM-DD

Scanned: [list of config types and item counts]

## Relocations

### 1. [Title]
- **Current:** ...
- **Recommended:** ...
- **Why:** ...
- **Impact:** ...

## Consolidations

### N. [Title]
...

## Net-New

### N. [Title]
...

## Correctly Placed

Per config type, state what was examined and why it's correctly placed. For items that were tested against a boundary (behavioral CLAUDE.md sections, imperative-voice memory files, project-vs-global scoping), show the reasoning in one line — not just "all correct."

Empty memory directories: note which projects have no memory files present.
```
