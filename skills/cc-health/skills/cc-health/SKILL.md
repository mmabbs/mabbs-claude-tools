---
name: cc-health
description: Audit Claude Code infrastructure health — config, skills/agents/plugins, memory, version compat, conversations, debris, temp files. Report-first, fix on confirmation.
argument-hint: chats|config|assets|memory|version|debris|temp|full
---

## When to Use

Trigger when:

- User asks to audit or maintain Claude Code configuration
- User invokes `/cc-health` with a domain or `full`
- SessionStart hook nudges about a version change (user follows up with `/cc-health version`)
- Periodic maintenance

## Domains

| Domain | Scanner | What it checks |
|--------|---------|----------------|
| `chats` | `cc-health-chats.py` | Conversations — scan, usage, clean, orphans |
| `config` | `cc-health-config.py` | Config files, scoping, permissions, MCP |
| `assets` | `cc-health-assets.py` | Skills, agents, plugins, workflows, trigger clashes |
| `memory` | `cc-health-memory.py` | MEMORY.md entries, stale paths |
| `version` | (orchestrated inline) | Changelog classification, compat checks |
| `debris` | `cc-health-debris.py` | Orphaned files, dead refs, TODO markers |
| `temp` | `cc-health-temp.py` | Scratch files, worktrees, droppings |
| `full` | (all of the above) | Run every domain sequentially |

## Workflow

### Step 1: Parse invocation

Extract the domain from the user's message. If no domain is specified, ask which domain to run or suggest `full`.

Accepted forms:
- `/cc-health config`
- `/cc-health chats --clean --empty-only`
- `/cc-health assets --deep`
- `/cc-health full`

### Step 2: Run scanner

For all domains except `version`:

```bash
python3 ~/.claude/plugins/local/cc-health/scripts/cc-health-<domain>.py [flags]
```

The script outputs JSON to stdout. Parse it as the finding report.

For `chats` domain, pass the flag as a positional argument:
```bash
python3 ~/.claude/plugins/local/cc-health/scripts/cc-health-chats.py scan [--project PATH] [--exact] [--filter-command CMD] [--empty-only]
python3 ~/.claude/plugins/local/cc-health/scripts/cc-health-chats.py clean [--confirm]
python3 ~/.claude/plugins/local/cc-health/scripts/cc-health-chats.py usage
python3 ~/.claude/plugins/local/cc-health/scripts/cc-health-chats.py orphans
```

For `full` mode, run each domain sequentially and aggregate findings.

**Chats output translation:** The chats scanner outputs its own legacy JSON format (a list of conversation objects), NOT the AuditReport schema used by other domains. When aggregating for `full` mode, do NOT treat chats output as Finding objects. Instead, summarize it as: conversation count, short-lived session count, orphan count, and total disk usage. Present this summary in a "Chats" section of the report alongside the other domains' finding tables.

### Step 3: Version domain (special handling)

The `version` domain does NOT have a standalone scanner script. Orchestrate it inline:

1. **Read state file:**
   ```bash
   cat ~/.claude/plugins/local/cc-health/state/.cc-health-state.json
   ```
   Extract `lastSeenVersion`.

2. **Read current version:**
   ```bash
   basename "$CLAUDE_CODE_EXECPATH"
   ```
   If the env var is unavailable, run `claude --version` and parse the version number.

3. **Check changelog freshness:**
   Read `~/.claude/cache/changelog.md`. Find the first `## X.Y.Z` heading. If that version is older than the current version, warn: "Changelog cache is stale — cannot classify accurately." and stop.

4. **Slice changelog:**
   Extract all content between `## <lastSeenVersion>` and `## <currentVersion>` (or from `## <lastSeenVersion>` to the top if currentVersion is the latest).

5. **Classify via agent:**
   Spawn the changelog-classifier agent with the changelog slice:
   ```
   Agent({
     subagent_type: "changelog-classifier",
     prompt: "Classify these changelog entries:\n\n<slice>"
   })
   ```
   The agent returns JSON with classified entries (only breaking/deprecation/schema-change).

6. **Match against config:**
   For each classified entry, grep the user's config files for the relevant keyword:
   - `settings.json`, `settings.local.json` for setting keys and env vars
   - `~/.claude/skills/*/SKILL.md` for trigger keywords
   - `~/.claude/agents/*/AGENT.md` for model/effort references

7. **Report only relevant hits.**

8. **Update state file:** Set `lastSeenVersion` to current version, update `domainRuns.version` timestamp.

### Step 4a: Trigger clash detection

**Trigger clash detection:** The assets scanner always checks for overlapping skill trigger
descriptions using TF-IDF similarity. Pairs above the threshold (default 0.35, tunable via
`--clash-threshold`) are flagged as:
- `unmanaged-trigger-clash` (warning) — no routing override in `skill-routing.md`
- `managed-trigger-clash` (info) — routing override exists

Run with a custom threshold: `/cc-health assets --clash-threshold 0.25`

**Delta reporting:** Previously-seen clashes are suppressed on subsequent runs — only new
clashes are surfaced. Use `--all-clashes` to bypass delta and show everything (this also
resets the baseline for future runs).

### Step 4: Assets --deep (special handling)

When `assets` is invoked with `--deep`:

1. Run the regular scanner first (checks 1–4, 6).
2. For each skill found, spawn an inline agent to check description drift:
   ```
   Agent({
     model: "claude-opus-4-6",
     prompt: "Compare this skill's description frontmatter against what its body actually does. Does the description accurately represent the skill's behavior?\n\nDescription: <desc>\n\nBody:\n<body>\n\nRespond with JSON: {\"drifted\": bool, \"reason\": \"...\"}"
   })
   ```
3. Add findings for skills where `drifted: true`.

### Step 5: Present report

Format findings as a markdown report:

```markdown
## cc-health Report — <domain>

**Summary:** X errors, Y warnings, Z info

### Errors
| Check | Message | File | Suggested Action |
|-------|---------|------|-----------------|
| ... | ... | ... | ... |

### Warnings
| Check | Message | File | Suggested Action |
|-------|---------|------|-----------------|
| ... | ... | ... | ... |

### Info
| Check | Message | File | Suggested Action |
|-------|---------|------|-----------------|
| ... | ... | ... | ... |
```

If no findings: "No issues found in the <domain> domain."

### Step 6: Fix on confirmation (if requested)

After presenting findings, the user may ask to fix issues. For each actionable finding:

- **Deletions** (orphaned entries, stale files): confirm per-batch, then delete.
- **Scope changes** (MCP re-scoping): show the exact change, confirm, then apply.
- **Removals** (stale env vars, dead imports): show what will be removed, confirm, apply.

Never fix without explicit confirmation. Group similar fixes when count > 5.

## Constraints

- Report-first: scanners are read-only. Only fix after user confirmation.
- Skip `~/.claude/archive/` in all scans (it's intentionally "dead").
- Skip files modified in the last hour (active session protection) in chats/clean.
- Never delete the current active session.
- The `version` domain updates state AFTER reporting — never before (so re-runs are safe).

## Output Location

- Console: Always output report to conversation
- No file output by default

## Deferred to v2.1

- Config: settings.json launch-root placement detection
- Config: MCP subdirectory-loss detection (flagging when subdir launches would lose a server)
- Memory: dead flag/setting references (setting keys named in memory not in active config)
- Memory: fuzzy-match moved path suggestions
- Debris: dead @-imports across all CLAUDE.md files (currently in assets domain only)
- Debris: half-renamed identifier detection
- Temp: abandoned git worktree detection
