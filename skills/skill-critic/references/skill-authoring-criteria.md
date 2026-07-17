# Skill Authoring Criteria

Evaluation criteria for skill quality. Extracted from Anthropic's skill authoring best practices, reframed for critique — "what to flag" rather than "how to write."

## Token Efficiency

Claude is already smart. Only add context it doesn't already have.

**Critique signals:**
- Instructions that explain concepts Claude already knows (what PDFs are, how libraries work)
- Paragraphs that don't justify their token cost — the context window is shared with conversation history and other skills
- Verbose examples where a concise one would suffice

## Degrees of Freedom

Match specificity to the task's fragility. A well-calibrated skill uses different freedom levels for different parts of its instructions.

**Decision test:** "If Claude does this differently than intended, what happens?"
- **"It breaks"** → low freedom. Deviation causes failure: wrong output, broken state, data loss. Provide exact specifications. Signal: external system dependencies, ordered operations, format specs.
- **"It's worse"** → medium freedom. Deviation degrades quality but the output still works. The process matters but multiple implementations can reach the same outcome. Signal: there's a right answer but more than one path.
- **"It's just different"** → high freedom. Deviation produces different but equally valid output. The goal is clear; the approach is a judgment call. Signal: creative work, communication style, organizational choices.

**Critique signals:**
- Bridge-level rigidity on a field task → flag as over-specified. Rigid MUSTs or exact templates for tasks where Claude's judgment produces good results.
- Field-level looseness on a bridge task → flag as under-specified. Vague language for fragile operations ("run the migrations in the right order"). If it bundles fragile operations as a script in `scripts/`, that's the right pattern.
- Validation rules left vague ("check the data is valid") when specific formats should be enforced → flag the mismatch.

## Progressive Disclosure

SKILL.md is an overview that points Claude to detailed materials as needed.

**Structural rules:**
- SKILL.md body under 500 lines. If approaching this limit, split into reference files with clear pointers about when to read them.
- References one level deep from SKILL.md. Nested references (SKILL.md → advanced.md → details.md) cause Claude to partially read files or skip them.
- Reference files over 100 lines should include a table of contents so Claude can see the full scope even when previewing.
- Agent prompt templates count as detailed content and belong in references/, not inlined in the body.

**Critique signals:**
- SKILL.md over 500 lines without progressive disclosure
- Reference chains deeper than one level
- Large reference files without a table of contents
- Agent prompts inlined in the body that could live in references/

## Description Quality

The description is the primary triggering mechanism. Claude uses it to choose the right skill from potentially 100+ available.

**Structural rules:**
- 1024 characters maximum (hard limit), 250 characters visible in `/skills` listing (display truncation)
- Include both what the skill does AND when to use it
- Name field: 64 characters maximum

**Critique signals:**
- Trigger-critical language truncated past 250 characters
- Third-person or passive descriptions (less effective than imperative "Use when...")
- Vague descriptions ("helps with documents") lacking specific trigger terms
- Negative triggers ("Do NOT use for X") without a real skill collision to justify them

## Structural Concerns

Questions to ask about specific skill features. Not every skill needs all of these — the question is whether the absence is a gap given what the skill does.

### Troubleshooting Coverage

**Ask:** Does this skill interact with external services (APIs, databases, CLI tools) or have multi-step setup that can fail?

**If yes, check:** Does it include troubleshooting covering common failure modes? Symptom/cause/fix structure, not generic "check the logs."

### Script Self-Sufficiency

**Ask:** Does this skill bundle executable scripts?

**If yes, check:** Do scripts handle their own errors with actionable messages, or do they fail silently? Scripts should capture both body and status code from HTTP calls, provide per-failure-mode error messages, and exit with clear failure indication.

**Flag:** Scripts that just crash and leave Claude to interpret raw error output.

### Pacing Guidance

**Ask:** Is this skill used for tasks where the quality/speed tradeoff matters?

**If yes, check:** Does it include explicit pacing direction? Analysis/review tasks benefit from "prioritize accuracy over speed." High-volume processing benefits from "prioritize throughput, flag edge cases for manual review."

**Flag:** Analytical skills with no pacing guidance (may produce rushed output). Batch-processing skills with no throughput guidance (may over-analyze each item).

### Time-Sensitive Patterns

**Ask:** Does this skill reference APIs, libraries, or tools that change across versions?

**If yes, check:** Does it handle deprecated patterns? Are there version-specific instructions that could become outdated?

**Flag:** Specific API syntax without version context — training data may contain outdated patterns.

### Magic Numbers

**Ask:** Does this skill use numeric constants (timeouts, batch sizes, retry delays)?

**If yes, check:** Is the rationale documented? Could Claude or a future maintainer understand why the value was chosen?

**Flag:** Unexplained constants (`timeout = 47` with no reasoning).

## Content Quality

### Terminology Consistency

Choose one term and use it throughout. Mixing "API endpoint," "URL," "API route," and "path" for the same concept confuses Claude's instruction-following.

**Flag:** Inconsistent terminology for the same concept within a skill.

### Option Overload

Don't present multiple approaches unless necessary. Provide a default with an escape hatch for specific cases.

**Flag:** "You can use X, or Y, or Z, or..." without a recommended default.

### Workflow Structure

Complex operations should be broken into clear sequential steps. Quality-critical tasks should include feedback loops (run validator → fix → repeat).

**Flag:** Complex multi-step workflows without step tracking. Quality-critical tasks without validation loops.
