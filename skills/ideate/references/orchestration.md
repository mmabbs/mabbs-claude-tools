# Orchestration Reference

How to execute combinations. The skill dispatches here whenever two or more modes are invoked together.

## Role Dispositions

Inject the appropriate disposition into every agent prompt. These are the exact instructions that establish each agent's relationship to context.

**Generative:**
> You are generating ideas. Commit fully to each direction. Do not second-guess, qualify, or preemptively critique your own output. Your job is to build forward with conviction. Other agents will challenge your work later — that is not your concern.

**Adversarial:**
> You have no investment in the material you are examining. You did not create it. Your job is to find what is wrong, what is missing, what was assumed without justification. Be thorough and unsparing. Constructive criticism is still criticism — don't soften it.

**Integrative:**
> You have access to everything that has been produced. Your job is to see the full picture — all outputs, all critiques, all tensions. Synthesize without flattening. Preserve productive disagreement. Your output should be richer than any single input.

## In-Context Execution

**When:** Solo modes and same-role combinations.

1. Load the first mode's reference file
2. Run the framework against the problem
3. If a second mode is specified, load its reference file
4. Run the second framework with the first step's output visible
5. Present combined output

No agents. No isolation. The second step SHOULD see the first step's reasoning — that's the point for same-role work.

## Cross-Role Two-Mode Execution

**When:** Two modes from different roles. Ask the user before deciding execution mode.

**Prompt template for asking:**
> This is a cross-role combination ({role1} → {role2}). I can run it two ways:
> - **In-context** — faster, you see the full reasoning chain, but the {role2} step may be influenced by seeing the {role1} reasoning
> - **Independent agents** — stronger {role2} independence (it only sees the {role1} conclusions, not the reasoning chain), but you'll see summaries rather than the full process
>
> Which do you prefer?

**Default recommendation:** If the problem is exploratory (brainstorming, open-ended), suggest in-context. If evaluative (stress-testing a plan, challenging a decision), suggest agents.

### In-Context Path

Run sequentially as with same-role, but frame the transition with the second mode's role disposition:

> "Now switching to adversarial lens. Examining this output with fresh eyes — no attachment to how it was built."

This doesn't create true independence but signals the cognitive shift.

### Agent Path

1. Spawn first agent via Agent tool (model: `opus`) with:
   - Role disposition (from section above)
   - Full contents of the mode's reference file
   - Problem context from the user
2. First agent produces output in-conversation (no notes for two-mode)
3. Spawn second agent via Agent tool (model: `opus`) with:
   - Its role disposition
   - Its mode reference
   - First agent's **conclusions only** — strip the reasoning chain. Pass what was produced, not how it was arrived at.
4. Present both outputs in-context with synthesis

## Three-Mode Pipeline Execution

**When:** Three modes from different roles. Always spawn agents — no in-context option.

### Pipeline Sequence

1. **Confirm output location.** Before spawning any agents, ask the user where pipeline notes should be saved. Default suggestion: current working directory. Pass the confirmed path to each agent.

3. **Parse the pipeline.** Identify which modes belong to which roles. Any ordering works, but the typical shape is Generative → Adversarial → Integrative.

4. **Spawn generative agent(s).** If the pipeline has multiple generative modes, spawn them in parallel (multiple Agent tool calls in one message). Each agent gets:
   - Generative disposition
   - Its specific framework reference
   - The problem context
   - Instruction to write full output as a note (see conventions below)

5. **Collect generative outputs.** Extract conclusions — not reasoning chains.

6. **Spawn adversarial agent.** Single Agent tool call. Gets:
   - Adversarial disposition
   - Its framework reference
   - ONLY the generative conclusions
   - Instruction to write critique as a note

7. **Spawn integrative agent.** Single Agent tool call. Gets:
   - Integrative disposition
   - Its framework reference
   - ALL previous outputs — generative AND adversarial, full text (integrative agents benefit from maximum context)
   - Instruction to write synthesis as a note

8. **Present in-context.** Summarize the synthesis with links to all notes.

## Output Note Conventions

For three-mode pipeline output only. Two-mode combinations produce output in-conversation.

**Filename:** `{topic slug} - {mode name}.md`
**Location:** The path confirmed with the user in step 1 of the pipeline sequence.

**Frontmatter (adapt to your project's conventions):**
```yaml
---
tags: [ideate, {mode-name}, {role}]
---
```

Add any additional metadata your project uses (note types, domains, cross-references). The skill doesn't enforce a schema — structure the output to fit your workflow.

## Agent Prompt Template

Literal template for composing Agent tool calls. Fill in the bracketed fields.

```
You are performing structured ideation using the {framework name} framework.

ROLE: {Generative | Adversarial | Integrative}
{role disposition text — copy from Role Dispositions section above}

FRAMEWORK:
{full contents of the mode's reference file}

PROBLEM:
{user's problem description}

{include only for adversarial or integrative agents:}
PRIOR WORK:
{conclusions from previous pipeline stages — NOT their reasoning chains}

OUTPUT:
- Apply the framework above to the problem
- {if generative: Build forward with full commitment. Do not hedge.}
- {if adversarial: Examine what was produced. Find weaknesses without mercy.}
- {if integrative: Synthesize all inputs. Preserve tensions that are productive.}
- {if three-mode pipeline: Write your full analysis as a note at {path}}
- {if three-mode pipeline: Use frontmatter — tags: [ideate, {mode}, {role}], plus any project-specific metadata}
- Do not pad. Do not invent structure to look thorough. If a section has nothing to say, say one line and move on.
- "Null is valid" — if you cannot find evidence for a claim, say so. Do not fill the gap with extrapolation.
```

**Model requirement:** All agents run on Opus. These frameworks are reasoning-intensive — they require the model to hold a problem's full structure, commit to a cognitive disposition, and produce output that withstands adversarial scrutiny from other agents. Lower-tier models produce shallow or generic output that defeats the purpose of structured ideation. If Opus is unavailable, solo modes (no agents) will still function but expect degraded quality; combinations and pipelines are not recommended.
