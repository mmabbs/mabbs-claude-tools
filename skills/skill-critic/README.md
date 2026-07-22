# skill-critic

Adversarial design review for Claude Code skills. Point it at a skill folder and it runs a structured critique: an adversary argues the strongest case against the skill's design, a defender evaluates each criticism honestly, a blind tester attempts a real task using only what the SKILL.md says — and the orchestrator cross-references all three into a verdict with proposed fixes.

1. Structural validation (`scripts/quick_validate.py`) — frontmatter, description budget, file references, orphaned resources
2. Steelman and blind-tester run in parallel — adversarial critique list + fresh-eyes task walkthrough
3. Defender rates each criticism: STRONG (keep as-is), WEAK (fix it), or UNCERTAIN
4. Synthesis — criticisms, defenses, and empirical friction cross-referenced into fixes, flagged items, and kept items
5. Post-fix validation confirms no structural regression

## Sample output

> **Fixes (defender rated WEAK):**
> 1. **Description budget overrun.** The description is 287 chars; the `/skills` listing truncates at 250. Truncated text contains the trigger phrase "meeting notes." Proposed: cut the second example clause (saves 41 chars).
>
> **Flagged for you (defender STRONG, blind-tester friction):**
> 2. **Step 3 config ambiguity.** Defender argues the config path is inferable; blind-tester independently stalled at the same step. Empirical friction overrides theoretical defense — recommend naming the file explicitly.
>
> **Kept (defense held):** 5 criticisms, summary table below.

## Requirements

| Component | Required? | Without it |
| --- | --- | --- |
| Claude Code | Required | — |
| The three agent files (see Installation) | Required | Every steelman/defender/blind-tester spawn fails |
| Opus-class model access | Optional, highly recommended | Critique quality drops noticeably — see note below |
| Python 3 + `pyyaml` | Optional | The structural validation steps fail; the critique flow itself still runs |

**Why Opus, and why "optional":** adversarial critique doesn't *use* reasoning as one ingredient — it is nothing but reasoning. That's the recommendation. It stays optional because model economics shift under your feet: what's expensive this quarter may be the budget tier next. The agent files pin `claude-opus-4-6` deliberately rather than the `opus` alias — an alias silently upgrades you to the newest Opus, which changes cost and behavior without asking. Bump the pin on purpose, not by accident.

## Installation

```bash
git clone https://github.com/mmabbs/mabbs-claude-tools.git
cp -r mabbs-claude-tools/skills/skill-critic ~/.claude/skills/
cp ~/.claude/skills/skill-critic/agents/*.md ~/.claude/agents/
pip install pyyaml   # optional — enables structural validation
```

Invoke with the skill name and a path: `skill-critic <path-to-skill-folder>`. This skill is user-invoked — it does not trigger on its own.

## Configuration

- **Effort.** The SKILL.md ships with no `effort` frontmatter, so it inherits your session default. Add `effort: high`, `effort: xhigh`, or `effort: max` to taste — higher tiers buy deeper critique on complex skills and cost accordingly; simple skills don't need the top tier.
- **Agent model pins.** All three agent files pin `claude-opus-4-6`. Edit the `model:` line in each to change tiers or update the pin.

## Pairs with skill-creator

Anthropic's skill-creator plugin and this skill are complementary halves: skill-creator builds skills and benchmarks them with eval runs; skill-critic stress-tests the *design* — ambiguity, gaps, over-specification — without executing anything. A natural chain is skill-creator to build, skill-critic to harden. It's also the cheaper of the two to run repeatedly, since it spawns three agents and no eval fleet.

## Bundled files

| File | Purpose |
| --- | --- |
| `SKILL.md` | The critique flow — orchestrator instructions |
| `agents/skill-critic--steelman.md` | Adversarial critique generator (install to `~/.claude/agents/`) |
| `agents/skill-critic--blind-tester.md` | Fresh-eyes task walkthrough (install to `~/.claude/agents/`) |
| `agents/skill-critic--defender.md` | Honest per-criticism defense (install to `~/.claude/agents/`) |
| `references/content-patterns.md` | Degrees-of-freedom framework and agent-architecture critique criteria |
| `references/skill-authoring-criteria.md` | Critique signals: token efficiency, progressive disclosure, description quality |
| `scripts/quick_validate.py` | Structural validator (frontmatter, references, orphans) |

## Changelog

### 2026-07-22

- Self-review release: ran skill-critic on itself (steelman: 9 criticisms; defender: 5 WEAK, 2 UNCERTAIN, 2 STRONG; blind-tester: fresh-install walkthrough).
- Fixed a broken validator invocation — `${CLAUDE_SKILL_DIR}` is not a real environment variable. The instructions now use the skill's base directory, which Claude Code states when the skill loads.
- Preparation now verifies the three agent files are installed before any spawn, so a skipped install step fails with a clear diagnostic instead of a cryptic runtime error.
- Abort-on-agent-failure clarified to "any of the three agents" and now states its reasoning: the synthesis's value is triangulation across three perspectives, and partial output can read as convincing while its claims go untested.
- Validator upgrades: missing `pyyaml` skips with an actionable message instead of a traceback; new bundled-agent coverage check (agent types spawned in SKILL.md must have a matching `agents/<name>.md`, unspawned bundles warn as orphans); usage message echoes the actual invocation.
- Blind-tester prompt spec now includes the skill's file path; the Context input may include a test scenario for the blind-tester.
- Description broadened ("pre-existing" dropped); steelman agent declares explicit `tools: Read, Glob, Grep`; corrected a stale self-reference in `references/content-patterns.md`.

### 2026-07-17

- First public release. Portable script paths, bundled agent definitions, validator accepts the `effort` frontmatter field.
