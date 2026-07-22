# config-audit

A placement auditor for your Claude Code configuration. It scans every config layer — rules, skills, hooks, plugins, MCP servers, memory, CLAUDE.md, agents — and answers one question: **is each piece of config stored in the layer that best serves it?**

It is most useful after a setup has grown organically: instructions duplicated between CLAUDE.md and rules, behavioral memories that should be rules, project-scoped config that belongs globally (or the reverse), procedures squatting in always-loaded files.

The workflow:

1. Locates eight criteria docs that define what earns its keep in each config layer and the boundary tests between adjacent layers — read by the reasoning agent, not the orchestrator.
2. Spawns eight scanner agents in parallel (one per config type, on Sonnet) that inventory every item with its purpose, cross-references, and content character (behavioral, context, pointer, procedural, enforcement).
3. Spawns a single reasoning agent (on Opus, max effort) that reads all inventories plus all criteria docs and writes findings to a session workspace file.
4. Presents findings in three categories — relocations, consolidations, net-new — plus a "Correctly Placed" section, so silence is never ambiguous.
5. Executes only the findings you choose to act on. Originals are archived, never deleted.

## Sample output

```markdown
## Relocations

### 1. `commit-conventions` section in project CLAUDE.md → rule with `paths:`
- **Current:** project CLAUDE.md, section "Commit Conventions" (behavioral)
- **Recommended:** `.claude/rules/commit-conventions.md` with `paths: ["**/*"]` narrowed to repo dirs it governs
- **Why:** rules boundary — path-scopable standing instruction paying always-on tokens
- **Impact:** suboptimal — works today, but costs every conversation ~120 tokens

## Consolidations

### 2. Release workflow spread across a skill, two hooks, and a helper script
- **Items:** `release-notes` skill, PostToolUse version-bump hook, Stop changelog hook, `scripts/tag.sh`
- **Workflow:** cutting a release
- **Recommended form:** plugin — single toggle, shared namespace, one install for other machines

## Net-New

### 3. None — no convergent evidence across layers this run.

## Correctly Placed

- **Rules:** `testing-policy.md` — behavioral, applies to all files, correctly unscoped.
- **Memory:** no files present in project `web-platform`.
```

## Requirements

| Component | Required? | Without it |
| --- | --- | --- |
| Claude Code with subagent (Agent tool) support | Required | The parallel scan can't run; the skill is built around scanner agents |
| Access to Sonnet and Opus models | Optional | Scanners and reasoning fall back to your session model — results hold, cost/quality tuning is lost |
| A CLAUDE.md list of your project directories | Optional | The skill asks you which project directories to scan instead of discovering them |
| Project `.claude/` directories | Optional | Projects without one are still scanned for memory and CLAUDE.md; the project-config layer is just empty |

## Installation

```bash
git clone https://github.com/<your-fork>/<repo>.git
cp -R <repo>/skills/config-audit ~/.claude/skills/config-audit
```

Restart Claude Code (or start a new session) and run `/config-audit`.

## Usage

```
/config-audit                          # full sweep, findings in chat
/config-audit project <name>           # one project + global config
/config-audit save <dir>               # write findings to a dated note
/config-audit project <name> save <dir>
```

## Adapting

1. **Project discovery.** The skill looks for a list of project directories in your CLAUDE.md (any table or list of project paths works). If you don't keep one, it asks which directories to scan — adding a small "Projects" table to your global CLAUDE.md makes full sweeps hands-free.
2. **Boundary opinions.** The criteria docs encode opinionated defaults — notably "when the memory/rule boundary is fuzzy, resolve to memory." If you prefer more rules and less memory, edit `references/criteria-memory.md` — the reasoning prompt (`references/reasoning-prompt.md`) cites it rather than restating it, so one edit changes the policy.
3. **Platform.** The findings file opens with `open` on macOS or `xdg-open` on Linux; on other platforms, substitute your default opener.

## Honest expectations

Findings quality depends on how much config you actually have — a fresh setup produces a short "Correctly Placed" list and little else. Anthropic's `claude-automation-recommender` plugin covers the adjacent job (recommending *new* automations); this skill deliberately stays on placement of what already exists, and its net-new category requires convergent evidence from at least two config layers before recommending anything.

## Bundled files

| File | Purpose |
| --- | --- |
| `SKILL.md` | The skill: arguments, scan phases, workflow, output formats |
| `references/scanner-prompt.md` | Prompt template for the eight scanner agents, incl. inventory format |
| `references/reasoning-prompt.md` | Prompt template for the reasoning agent, incl. boundary sweeps |
| `references/criteria-rules.md` | What belongs in rule files; boundaries vs. CLAUDE.md, memory, skills, hooks |
| `references/criteria-skills.md` | What belongs in skills; boundaries vs. hooks, agents, rules, commands, memory |
| `references/criteria-hooks.md` | What belongs in hooks; enforcement vs. guidance, intentional rule/hook stacking |
| `references/criteria-plugins.md` | When loose config should become a plugin; install-state gotchas |
| `references/criteria-claude-md.md` | What belongs in CLAUDE.md; length discipline, layer boundaries |
| `references/criteria-mcp.md` | When an MCP server is warranted vs. CLI-via-Bash or scripts |
| `references/criteria-agents.md` | When a pattern deserves an agent definition; qualification threshold |
| `references/criteria-memory.md` | What belongs in memory files; red flags, staleness discipline |

## Changelog

### 2026-07-19

- Post-review refinements from an adversarial skill critique: description compressed under the 250-char listing truncation; scanner and reasoning prompt templates extracted to `references/`; reasoning agent now writes findings to the workspace file explicitly; memory-directory slug encoding documented; hooks scanner records plugin enabled state; plugin scanner pointed at install/enable state locations; orchestrator no longer loads criteria docs (reasoning agent reads them); reasoning prompt cites criteria docs instead of restating rules; "Correctly Placed" output grouped by config type; platform-neutral file-open instruction.

### 2026-07-17

- First public release. Sanitized from the author's personal setup: personal project names, plugin cross-references, and proactive invocation removed; project discovery generalized.
