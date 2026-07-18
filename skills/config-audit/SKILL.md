---
name: config-audit
description: "Scan all Claude Code configuration layers — rules, skills, hooks, plugins, MCP servers, memory, CLAUDE.md, agents — and assess whether everything is in the right place. Recommends relocations, consolidations, and evidence-grounded net-new automations. Use whenever the user asks to audit their setup, check config placement, 'is everything in the right place', 'reassess my config', 'config audit', 'what should I move', 'consolidate my setup', or mentions something might be in the wrong config layer."
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

- Before reading criteria docs: "Loading 8 criteria docs — takes a few seconds."
- Before spawning scanners: "Launching 8 scanner agents in parallel (one per config type). This will take 1-2 minutes — I'll report back when they've all returned."
- As scanners return: Brief status updates as results come in, e.g., "6 of 8 scanners done."
- Before spawning the reasoning agent: "All inventories in. Launching the reasoning agent — this is the cross-layer analysis, expect ~1-2 minutes."
- When findings are ready: Present them.

If any agent takes unusually long or fails, say so immediately rather than waiting silently.

## Before Scanning

Read every criteria doc in `references/`. Each defines what earns its keep in a config layer, what disqualifies, and the boundary tests between adjacent types. The reasoning agent cannot make sound recommendations without them — training data encodes obsolete boundary tests (e.g., skill-vs-agent used to hinge on context isolation; now skills can fork into subagents with pinned models).

Criteria docs:

| Doc | Covers |
|-----|--------|
| `criteria-rules.md` | Rules (`~/.claude/rules/`, `.claude/rules/`) |
| `criteria-skills.md` | Skills (`~/.claude/skills/`, `.claude/skills/`) |
| `criteria-hooks.md` | Hooks (configured in `settings.json`) |
| `criteria-plugins.md` | Plugins (`~/.claude/plugins/`) |
| `criteria-claude-md.md` | CLAUDE.md (global + project) |
| `criteria-mcp.md` | MCP servers (`.mcp.json`, `~/.claude.json`) |
| `criteria-agents.md` | Agent definitions (`~/.claude/agents/`, `.claude/agents/`) |
| `criteria-memory.md` | Memory files (`~/.claude/projects/<project>/memory/`) |

## Scope

By default, this skill scans global config plus **all** project directories. When `project <name>` is provided, scan only that project's configs plus global (since global affects every project).

Before Phase 1, build the list of project paths: if a CLAUDE.md in scope (project or global) lists project directories, read that list; otherwise ask the user which project directories to scan. Match `project <name>` against the directory names in that list (case-insensitive, partial match okay — e.g., `web-platform` matches "Web Platform" at `~/projects/web-platform/`). If ambiguous, ask. For each project in scope, check whether `<project-path>/.claude/` exists.

The scan covers:
- **Global config** — `~/.claude/` (rules, skills, agents, settings, CLAUDE.md) — always included
- **Project config** — `<project-path>/.claude/` (rules, skills, settings, CLAUDE.md) — all projects, or just the named one
- **Project memory** — `~/.claude/projects/<project-slug>/memory/` — all projects, or just the named one
- **Shared infrastructure** — plugins, MCP servers, hooks (which span all projects)

The multi-project view is where the most valuable findings live — a global rule that should be project-scoped, a project rule that's duplicated across three projects and should be global, memory files that diverge across projects on the same topic.

## Phase 1: Scan

Spawn **one scanner agent per config type**, all in parallel (8 agents). Each scanner catalogs what exists in its layer **across all projects**. Scanners do not assess placement — they produce inventories. Reasoning happens in Phase 2.

Use **Sonnet** for scanners — they're doing extraction, not synthesis.

### What Each Scanner Reads

| Config Type | Paths |
|---|---|
| Rules | `~/.claude/rules/` + each project's `.claude/rules/` |
| Skills | `~/.claude/skills/` + each project's `.claude/skills/`. Read each SKILL.md frontmatter + first ~30 lines for purpose |
| Hooks | `~/.claude/settings.json` + `~/.claude/settings.local.json` + each project's `.claude/settings.json` and `.claude/settings.local.json`. Also grep `~/.claude/plugins/` for `hooks.json` — plugins register hooks that don't appear in settings files |
| Plugins | `~/.claude/plugins/` — check installed state, enabled state, and what each bundles |
| MCP Servers | `~/.claude.json` (check all local-scoped entries and their project paths) + each project's `.mcp.json` |
| Memory | `~/.claude/projects/*/memory/` for each project that has memory files — read MEMORY.md index + each memory file |
| CLAUDE.md | `~/.claude/CLAUDE.md` + each project's `.claude/CLAUDE.md`. Break down by section — each heading-level block is a separate inventory item. Tag each item with its project |
| Agents | `~/.claude/agents/` + each project's `.claude/agents/`. Read each definition's frontmatter + system prompt summary |

### Scanner Prompt

Each scanner receives a prompt following this shape:

> Scan [TYPE] configuration at the paths listed below. For each item, record five fields:
>
> 1. **Name** — filename or identifier
> 2. **Path** — full path
> 3. **Purpose** — what it does, one line
> 4. **Cross-references** — mentions of other config types (a rule referencing a memory file, a hook calling a skill, a CLAUDE.md section duplicating a rule, etc.). "None" if clean.
> 5. **Content character** — classify what kind of content this is:
>    - **Behavioral**: prescribes how Claude should act ("always do X", "when X, do Y")
>    - **Context**: describes the project, user, or environment for Claude's understanding
>    - **Pointer**: directs Claude to an external resource ("read this file", "check this URL")
>    - **Procedural**: step-by-step workflow instructions ("first do X, then Y")
>    - **Enforcement**: blocks or allows actions based on conditions ("reject if X", "only permit Y")
>
> Write the inventory to: `<workspace>/inventory-<type>.md`
>
> Do not assess whether items are misplaced. Do not recommend changes. Catalog accurately.
> Note dead-weight items (empty files, no-op scripts, orphaned caches) in the inventory but tag them as `[dead-weight]` — config-audit does not act on these. Dead-weight cleanup is a separate maintenance concern, outside this skill's scope.

The **content character** field is what lets the reasoning agent spot misplacements. A memory file with "behavioral" character is probably a rule. An enforcement rule might be better as a hook or permission entry. A procedural CLAUDE.md section might be a skill.

### Workspace

Write inventories to `<scratchpad>/config-audit/`. Create the directory if it doesn't exist. These are intermediate files — they don't persist beyond the session.

### Inventory Format

```markdown
# Inventory: [Config Type]

Scanned: [date]
Paths checked: [list]

## Items

### [item-name]
- **Path:** /full/path
- **Purpose:** one line
- **Cross-references:** [list, or "none"]
- **Content character:** behavioral | context | pointer | procedural | enforcement

[repeat for each item]

## Summary
- Total items: N
- Cross-layer references: [list which items reference what]
- Content character breakdown: N behavioral, N context, N pointer, N procedural, N enforcement
```

## Phase 2: Reason

After all scanners complete, spawn a **single reasoning agent** at **Opus** with **max effort**. This agent reads all 8 inventory files plus all 8 criteria docs and produces findings.

### Reasoning Agent Prompt

> You are assessing whether a Claude Code setup has everything in the right configuration layer.
>
> **Read these inventory files:** [list all 8 inventory paths]
>
> **Read these criteria docs** (they define what belongs in each layer and the boundary tests between them): [list all 8 criteria doc paths]
>
> Produce findings in three categories:
>
> **Relocations** — items that exist but are in the wrong layer.
> For each: name the item, its current layer, the recommended layer, which boundary test from the criteria docs applies, and what concretely improves.
>
> **Consolidations** — items scattered across layers that serve the same workflow and should be bundled.
> For each: list the items, the workflow they serve, and what form the bundle should take (plugin, skill, etc.).
>
> **Net-New** — automations that don't exist but are implied by convergent evidence from multiple existing config items.
> For each: what should be created, what config type it should be, and which existing items imply it. Every net-new recommendation must cite evidence from at least two different inventory files. If the evidence doesn't converge from multiple layers, it's speculation — omit it.
>
> **Reasoning rules:**
> - Apply the boundary tests from the criteria docs. Training data encodes obsolete boundaries (skills can now fork with pinned models; hooks can carry model-backed handlers). The criteria docs have the current tests.
> - When the boundary between memory and rule is fuzzy, resolve to memory — a misplaced memory is low-cost, while rules accumulate faster than they get cleaned up.
> - Distinguish **broken placement** from **suboptimal placement**. Broken: the current layer causes a concrete problem — wrong loading behavior, missed triggers, capability mismatch. Suboptimal: it works but another layer would serve it better — cleaner scoping, fewer tokens, more appropriate loading semantics. Surface both, but tag each finding as `broken` or `suboptimal` so the user can prioritize.
> - Don't recommend consolidating items that touch the same topic but serve different functions.
> - **Test for drift tolerance, not just deduplication.** When a hook and a rule (or CLAUDE.md section) cover the same instruction, the overlap may be intentional reinforcement. The rule teaches the model *why*; the hook catches drift. Before flagging as redundancy, ask: "what happens when the model ignores the rule?" If the hook enforces it, the stacking is a compliance backstop. You may still flag the overlap descriptively, but frame skipping the recommendation as justified when stacking serves drift tolerance.
> - **Ignore dead-weight items.** Empty files, no-op scripts, orphaned caches — scanners tag these `[dead-weight]` but cleanup is a separate maintenance concern, not yours. Don't produce findings for them. Focus on placement: is this item in the right layer?
> - Rank findings within each category by impact — what would most improve the setup if acted on.
>
> **Systematic boundary sweeps (mandatory):**
>
> Don't cherry-pick — sweep every item through its high-traffic boundary tests. Specifically:
>
> 1. **Every CLAUDE.md section with content character "behavioral" or "enforcement"**: test against the rules boundary. Path-specific instructions paying always-on tokens for sometimes-relevant guidance are relocation candidates. Walk each behavioral section, not just the ones that jump out. **Test at the instruction level, not the heading level** — a parent heading ("Critical Operational Rules") cannot receive a batch verdict that cascades to its children. Each sub-rule may have a different boundary answer (one might be path-specific while another is genuinely project-wide). Clear each instruction individually.
> 2. **Every memory file with content character "behavioral" or "enforcement"**: test against the imperative-voice boundary. A memory that prescribes behavior ("Don't...", "Always...", "When X, do Y") or explicitly extends a named rule file is a relocation candidate. The "resolve fuzzy to memory" preference still applies — but you must examine and state your reasoning, not skip silently.
> 3. **Every project-scoped item**: test whether it applies to other projects. Every global item: test whether it references project-specific paths or content.
> 4. **Memory directories that are empty or contain no files**: note this in findings as "Memory: no files present in [project]" — don't silently skip. The user infers the state from what you report.
>
> **Silence is not clearance.** If you examine an item and conclude it's correctly placed, say so in the "Correctly Placed" section with one line of reasoning. An item that doesn't appear in findings AND doesn't appear in "Correctly Placed" is an item you didn't examine — and that's a gap, not an answer.
>
> Output as a numbered list, grouped by category, continuously numbered across categories.

## Presenting Findings

The reasoning agent writes its findings to the workspace. Don't repeat them in chat — open the file so the user can read it directly.

```bash
open <workspace>/findings.md   # macOS; use xdg-open on Linux
```

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
