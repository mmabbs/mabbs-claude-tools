---
name: skill-sanitizer
description: Ready a personal Claude Code skill for public GitHub release. Use when the user wants to sanitize, publish, stage, or release a skill. Copies to staging, strips personal data, applies portability fixes, writes the public README, gates the repo move.
argument-hint: <path-to-skill-folder>
effort: high
when_to_use: |
  I want to sanitize my skill for public release
  Get this skill ready for GitHub
  Publish this skill to my public repo
  Prepare a skill for sharing
  Strip personal data from this skill
---

# Skill Sanitizer

Transform a personal Claude Code skill into a copy ready for the public GitHub repo. All work happens on a staging copy — the live skill is never edited.

## Inputs

- **Path** (required): the skill folder to sanitize. Usually a live skill under `~/.claude/skills/` or an existing staging copy.
- **Context** (optional): known issues, areas of concern, or publishing history. Include in the message after the path.

## Ground Rules

- **Never edit the live skill.** Every transformation happens on the staging copy. Before any Edit or Write, check the file path starts with the staging directory. If it doesn't, stop.
- **Announce each stage as you enter it.** One line: stage name and what's about to happen. No silent gaps between stages.
- **Read `references/repo-conventions.md` before Stage 1.** It holds the staging and repo paths, the triage criteria, and the final gate checklist.
- **If running non-interactively** (no user available to confirm), apply the recommended option for each decision point and mark it `AUTO-APPLIED` in the report. Do not stall waiting for input that cannot come.

## Stage 1 — Canonicalize

Skills drift across copies. A staging copy from last month may be missing content the live skill gained since — or vice versa.

1. Locate every copy of the skill: the given path, `~/.claude/skills/<name>/`, and the staging directory. Ask the user if Desktop `.skill` exports or vault copies exist.
2. If more than one copy exists, diff them (`diff -ru`). Report qualitative differences — content one copy has that another lacks, not just whitespace.
3. Merge newer content into a single canonical version before sanitizing. Never silently pick one copy; show the user what differs and confirm the merge direction.

## Stage 2 — Read Everything, Then Assess

Read every file in the skill: SKILL.md, references, scripts, assets. No edits during this stage — findings presented before files change is what keeps the punch list complete.

Present findings in three buckets:

1. **Sanitization** — blocks repo entry: secrets, personal paths, names, vault coupling, proactive triggers.
2. **Polish** — professionalism: structure, artifacts, naming, stale content.
3. **What Needs Writing** — missing README, adaptation sections, install docs.

Flag secrets (API keys, calendar IDs, account identifiers) separately and first. They are a higher severity tier than paths or names.

## Stage 3 — Blockers and Advisories

The publish decision belongs to the user. By the time this skill is invoked, they have already judged the skill worth sharing — never veto that judgment with a verdict of your own. This stage reports two kinds of findings (definitions in `references/repo-conventions.md`):

1. **Blockers** — objective defects that make the copy non-functional for adopters: broken file references, missing scripts the SKILL.md depends on, referenced agents with no definition anywhere, half-built features. Blockers don't stop the sanitization work — they block the repo move at Stage 7 until resolved.
2. **Advisories** — observations the user should weigh, stated once and prominently, then dropped: "after sanitization every step is a placeholder — nothing but your configuration remains," "this overlaps heavily with built-in X." Advisories never block and are never re-argued. Present them and proceed.

## Stage 4 — Copy to Staging

Copy the canonical version into the staging directory. If a stale staging copy exists, replace it — Stage 1 already harvested anything newer from it. Work on this copy from here on.

## Stage 5 — Mechanical Pass

Read `references/mechanical-pass.md` and apply every item. These run unconditionally — no confirmation needed. They are transformations that were applied uniformly across every skill sanitized to date without a single reversal.

After the pass, report what changed as a numbered list grouped by file.

## Stage 6 — Judgment Pass

Read `references/judgment-pass.md` and work through each call. These are keep/remove decisions where past sanitization runs needed the user's correction — do not apply them silently.

Present all calls in one message: for each, the finding, your recommendation, and the reasoning. Apply only after the user decides.

## Stage 7 — Docs and Gate

1. Write the public README following `references/readme-template.md`.
2. Run the final sweep from `references/repo-conventions.md` — a grep for names, home paths, vault identifiers, and secret-shaped strings over the staging copy. Every hit gets resolved or explicitly justified to the user.
3. Only after the sweep is clean **and no blocker is unresolved**: copy the skill into the publish repo's `skills/` directory, add or update its entry in the repo README, and add a dated changelog entry per the conventions file. An open blocker keeps all completed work in staging and the report says exactly what needs building — nothing enters the repo.

The gate is one-way. Secrets and personal paths that reach git history are permanent even after a fixing commit — nothing moves to the repo until the sweep passes.

**The sweep is the last operation that touches the staging copy.** If anything executes in staging after it — a validator, a test run, any script — generated artifacts reappear (`__pycache__/` embeds absolute paths in bytecode) and the sweep is void. Delete generated artifacts and run the sweep again before the repo move.

## Stage 8 — Handoff

Two offers, neither automatic:

1. **Validation run**: offer to invoke skill-critic on the staged copy. If accepted, pass this context — and instruct the orchestrator to include it in the steelman and defender prompts only, never the blind-tester's: "This skill is designed for public distribution. Absent user-specific paths, unset config values, and 'replace with your own' placeholders are intentional — do not flag them as gaps." The blind-tester stays unmodified because it simulates a genuinely fresh user.
2. **Commit**: offer to commit the repo changes. Show the diff summary first.

Close with a one-paragraph report: outcome (published, or held in staging with blockers named), counts per pass, advisories raised, what was written, what's pending.
