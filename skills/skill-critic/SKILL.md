---
name: skill-critic
description: Critique and refine Claude Code skills. Use when reviewing a skill's instructions for gaps, ambiguity, or structural issues. Runs adversarial critique, structured defense, and blind usability testing, then proposes targeted fixes.
argument-hint: <path-to-skill-folder>
---

# Skill Critic

## Table of Contents

- 01 Skill Anatomy
- 02 Inputs
- 03 Critique Flow
  - 03.1 Preparation
  - 03.2 Adversarial Critique + Blind Test
  - 03.3 Defense
  - 03.4 Synthesis
  - 03.5 Post-fix Validation
- 04 Assessment Rubric
  - 04.1 Description Quality
  - 04.2 Body Quality
  - 04.3 Agent Architecture
  - 04.4 Structural Checklist
- 05 Scripts Reference

Critique and refine Claude Code skills through adversarial review, structural validation, and targeted fixes.

## 01 Skill Anatomy

A skill is a SKILL.md file (plus optional bundled resources) discovered through a three-level loading system:

1. **Metadata** (name + description) — always in context. This is how Claude decides whether to use the skill. If the description is weak, the skill never fires.
2. **SKILL.md body** — loaded when the skill triggers. This is the instruction set.
3. **Bundled resources** (references/, scripts/, assets/) — loaded as needed. Scripts can execute without entering the context window.

The description is the most important line in any skill. Everything else is wasted if Claude never reads it.

## 02 Inputs

- **Path** (required): path to the skill folder being critiqued. Pass as the argument after the skill name.
- **Context** (optional): comments for the orchestrator and/or sub-agents — what the skill is for, known issues, areas of concern, recent failures. May include a test scenario for the blind-tester to attempt. Include in the message body after the path.

## 03 Critique Flow

Prioritize thoroughness. A shallow critique that misses real gaps is worse than a slow critique that catches them.

<NO-SUMMARIZE>
All agent prompts in this flow must include the full SKILL.md text inlined — never summarized. Summaries strip exact wording, and an installed copy may differ from the version under review, invalidating every verdict downstream.
</NO-SUMMARIZE>

**Orchestrator role:** You are a neutral judge. You prepare the inputs, dispatch three agents (steelman, blind-tester, defender), and synthesize their outputs into a verdict. You do not author critiques — the steelman does that. You do not defer to any single agent's judgment — the synthesis is yours to weigh. When agents disagree, you evaluate the evidence and decide. When no agent catches something, you can surface it yourself as a new finding.

### 03.1 Preparation

Read the SKILL.md at the provided path. Read all bundled resources (references/, scripts/, assets/) to understand the full picture. Note the skill's stated purpose and intended triggers.

Run `scripts/quick_validate.py` against the skill directory:

    python <skill-base-dir>/scripts/quick_validate.py <path-to-skill>

`<skill-base-dir>` is this skill's own base directory — Claude Code states it when the skill loads.

The script checks frontmatter validity, description length, body word count, referenced file existence, orphaned resources, and bundled agent coverage. Record any failures or warnings — they feed into the critique.

Verify the three agent types this flow spawns — `skill-critic--steelman`, `skill-critic--blind-tester`, `skill-critic--defender` — are installed (their definition files exist in `~/.claude/agents/`). If any are missing, stop and point the user to the README's installation steps; every spawn below would otherwise fail.

### 03.2 Adversarial Critique + Blind Test

Spawn two agents in parallel:

**Steelman** (subagent_type: `skill-critic--steelman`): Generates the adversarial critique list. The prompt must include:

- The full SKILL.md text, inlined — summaries strip exact wording, and if the agent goes looking for the file itself, an installed copy may differ from the version under review, invalidating every verdict it touches
- The file path so the agent can read bundled resources
- The Assessment Rubric (see 04) as evaluation criteria
- The authoring criteria in `references/skill-authoring-criteria.md` — additional critique signals: token efficiency, progressive disclosure, description quality, terminology consistency
- Structural validation results from the preparation step
- Any contextual comments from the user
- Instruction: "Produce a numbered critique list arguing against this skill's design. For each item, identify what's ambiguous, what could fail, what's underspecified, what's over-specified. Always include a description budget check — the /skills listing truncates at 250 characters."

**Blind-tester** (subagent_type: `skill-critic--blind-tester`): Tests the skill from a fresh perspective. The prompt must include:

- The full SKILL.md text, inlined — same rule as the steelman
- The file path so the agent can read bundled resources — its scope constraint depends on receiving it
- A representative task that exercises the skill's primary flow end-to-end. Construct a plausible user prompt for the skill's most common use case, not an edge case — a bad task produces a blind-test that misses real gaps regardless of skill quality.
- Any contextual comments from the user

Present the steelman's critique list to the user.

### 03.3 Defense

Spawn agent type `skill-critic--defender`. The prompt must include:

- The full SKILL.md text, inlined — never summarize
- The file path so the agent can read bundled resources if needed
- The steelman's numbered critique list
- Any contextual comments from the user

The defender returns verdicts per criticism: **STRONG** (keep as-is), **WEAK** (fix it), or **UNCERTAIN** (needs testing). A description over 250 characters should be treated as WEAK unless the truncated portion is demonstrably redundant.

### 03.4 Synthesis

If any of the three agents failed (crashed or returned unusable output), report the failure to the user and abort. The run is forfeit — start fresh in a new session. The synthesis's value is triangulation across three independent perspectives; with one missing, the surviving output can still read as convincing while its claims go untested — exactly the unexamined-opinion failure this skill exists to prevent.

Cross-reference steelman critiques, defender verdicts, and blind-tester findings:

- **Defender WEAK** → fix. Include a suggested fix with a concrete proposed change.
- **Defender STRONG, but blind-tester reports empirical confusion on the same point** → flag for the user with both the defense and the blind-tester's walkthrough evidence. Empirical friction can override theoretical defense because the blind-tester's confusion is evidence the defender's reasoning didn't account for.
- **Defender STRONG, no contradicting evidence** → keep as-is.
- **UNCERTAIN** → flag for the user with evidence from both sides.
- **Blind-tester findings not in the steelman's critique list** → add as new findings. Include a suggested fix for each.

When proposing fixes, apply the Refinement Principles:

- **Generalize from specific failures** — if a specific case fails, ask what _category_ of case it represents, then fix the category. Don't patch the instance.
- **Look for repeated work** — if Claude would keep writing the same helper script across invocations, it should be bundled in scripts/.
- **Remove what isn't pulling weight** — dead sections, steps Claude skips, instructions that produce unproductive work. Leaner is better.
- **Stop when it works** — a skill that handles 90% of cases well is better than one that handles 100% and is bloated.

**Presentation:**

- Group by category: fixes first, then uncertain items, then new findings, then kept items as a summary table.
- Order fixes by impact, highest severity to lowest. For each fix, include reasoning for why it ranks where it does in the severity hierarchy.
- Number findings sequentially within each group (1, 2, 3...) — internal numbering from the steelman's list does not carry to user-facing output.
- For fixes where the defender rated STRONG but blind-tester evidence or orchestrator analysis overrides, show the defender's position and the override reasoning explicitly.
- New findings from the blind-tester must each include a suggested fix.

Present the synthesis with proposed changes and wait for user approval before applying any edits.

### 03.5 Post-fix Validation

After applying fixes, re-run `quick_validate.py` to confirm no structural regression (e.g., a revision broke a file reference or pushed the description past 250 characters).

## 04 Assessment Rubric

Criteria the steelman evaluates against when generating its critique.

### 04.1 Description Quality

- **250-character budget** — the `/skills` listing truncates at 250. What gets truncated? Is the lost text trigger-critical?
- **Imperative framing** — "Use when the user wants to..." triggers better than third-person or passive descriptions.
- **Abstract verbs** — prefer verbs that subsume multiple phrasings ("create, build, write, improve") over listing every possible user phrasing. Breadth through well-chosen vocabulary, not exhaustive examples.
- **Negative trigger economy** — "Do NOT use for X" only when there's a real collision with another skill. Each negative trigger eats into a tight budget.
- **Undertrigger bias** — Claude tends to undertrigger. Descriptions should err toward breadth.

### 04.2 Body Quality

- **Imperative form** — instructions use imperative/infinitive ("Start by reading..." not "You should start by reading...")
- **Reasoning over rigidity** — explain the _why_ behind instructions. Claude responds better to reasoning than rigid MUSTs because it can generalize from understood intent rather than pattern-matching against rigid rules.
- **Specificity matched to fragility** — high freedom for judgment calls, low freedom for operations where deviation causes failure. When evaluating specificity levels, reference `references/content-patterns.md` for the Degrees of Freedom framework.
- **Token efficiency** — if Claude already knows it, it shouldn't be in the skill. The context window is shared with the user's conversation.
- **Word count** — body should target 1,500–2,000 words. Detailed content (including agent prompt templates) belongs in references/.

### 04.3 Agent Architecture

Evaluate when the skill spawns sub-agents via the Agent tool. Not every skill uses agents — skip this section entirely when it doesn't apply.

- **Orchestration test** — Does the parent do real work with the agent's output (evaluate, branch, synthesize, transform), or relay it verbatim? A pass-through parent adds token overhead and latency for zero gain. When evaluating orchestration patterns, reference `references/content-patterns.md` for the full framework.
- **Inline viability** — Could the work be done within the skill's own execution? Agent isolation is justified for parallel work, adversarial independence, model-tier optimization, or genuine context isolation — not as a default.
- **Prompt self-containment** — Would a contractor produce good work from the agent prompt alone, with no access to the preceding conversation? If the prompt relies on context the agent won't have, results will be shallow or invented.
- **Bundled vs. named choice** — If the skill uses agents, is the right kind used? Bundled agents (prompts inline or in references/) suit one-off helpers specific to this skill. Named agents (`~/.claude/agents/`, spawned by type) suit agents with distinct roles, independent utility, or their own config needs. Also flag if the skill reimplements what an existing named agent already does.

### 04.4 Structural Checklist

These are questions, not requirements — not every skill needs all of these:

- Does this skill spawn agents? If so, does the parent do real orchestration, or is it a pass-through?
- Does this skill interact with external services but lack a troubleshooting section?
- Are there magic numbers or unexplained configuration values without rationale?
- Do bundled scripts handle their own errors, or do they punt to Claude?
- Does the skill include pacing guidance appropriate to the task (careful analysis vs. high-throughput processing)?
- Are there time-sensitive patterns that could become outdated?

## 05 Scripts Reference

Run with `python <skill-base-dir>/scripts/<name>.py` — works from any directory. `<skill-base-dir>` is this skill's base directory, stated when the skill loads.

| Script              | Purpose                                  | Dependencies |
| ------------------- | ---------------------------------------- | ------------ |
| `scripts/quick_validate.py` | Structural validation of skill directory | `pyyaml`     |

**Prerequisites:** `pip install pyyaml`.

