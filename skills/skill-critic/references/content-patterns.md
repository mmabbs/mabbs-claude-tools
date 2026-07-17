# Critique Reference: Content Patterns

Use this reference when evaluating whether a skill's instructions are at the right specificity level, and whether it handles common structural concerns.

## Degrees of Freedom

Evaluate whether a skill gives Claude the right amount of direction — not too much, not too little.

### The Bridge vs. Field Analogy

**Crossing a field:** Many paths lead to the destination. Give general direction, let Claude choose the route.

**Building a bridge:** Precise engineering required. Deviation causes failure. Provide exact specifications.

A well-calibrated skill uses different freedom levels for different parts of its instructions. The critic's job is to flag mismatches: bridge-level rigidity on a field task (over-specified), or field-level looseness on a bridge task (under-specified).

### High Freedom — When Multiple Approaches Work

Appropriate when Claude's judgment produces good results and the "how" matters less than the "what."

**Example — documentation skill:**
```markdown
## Writing Style
Write documentation in clear, accessible language. Use examples to illustrate
complex concepts. Organize content logically with appropriate heading levels.
```

Claude knows how to write. Specifying exact sentence structures would be over-constraining.

**Example — code review skill:**
```markdown
## Review Focus
Examine code for correctness, readability, and potential edge cases.
Suggest improvements where the benefit is clear.
```

**Critique signal:** If a skill uses rigid MUSTs or exact templates for tasks like these, flag it as over-specified.

### Medium Freedom — Process Matters, Details Flexible

Appropriate when certain steps must happen but order or exact method can vary.

**Example — data validation:**
```markdown
## Validation Process
1. Load the input file (CSV, JSON, or YAML supported)
2. Check required fields exist: `name`, `id`, `timestamp`
3. Validate field formats:
   - `id`: alphanumeric, 8-12 characters
   - `timestamp`: ISO 8601 format
4. Report validation errors with line numbers
5. Output clean data to `output/validated.{format}`
```

Specifies WHAT to validate but lets Claude choose HOW to implement.

**Critique signal:** If a skill leaves validation rules vague ("check the data is valid") or over-specifies the implementation ("use regex pattern X for the id field"), flag the mismatch.

### Low Freedom — Deviation Causes Failure

Appropriate for fragile operations, external service requirements, or operations where debugging is difficult.

**Example — database migration:**
```bash
#!/bin/bash
set -euo pipefail
# Must run in this order - foreign key dependencies
psql -f migrations/001_users.sql
psql -f migrations/002_organizations.sql
psql -f migrations/003_user_org_memberships.sql
psql -c "SELECT COUNT(*) FROM schema_migrations;"
```

No room for improvisation. Dependencies mean order matters.

**Critique signal:** If a skill uses vague language for operations like these ("run the migrations in the right order"), flag it as under-specified. If it bundles fragile operations as a script in `scripts/`, that's a good pattern.

## Structural Checklist

These are questions the critic asks about specific skill features. Not every skill needs all of these — the question is whether the *absence* is a gap given what the skill does.

### Troubleshooting Coverage

**Ask:** Does this skill interact with external services (APIs, databases, CLI tools) or have multi-step setup that can fail?

**If yes, check:** Does it include a troubleshooting section covering common failure modes? Are error messages actionable (symptom → cause → fix), or does the skill leave Claude to guess?

**What "good" looks like:** Symptom/cause/fix structure for each common failure. Not a generic "check the logs" — specific commands and expected output.

### Script Self-Sufficiency

**Ask:** Does this skill bundle executable scripts?

**If yes, check:** Do the scripts handle their own errors with actionable messages, or do they fail silently or with cryptic output that Claude has to interpret?

**What "good" looks like:**
- Captures both body and status code from HTTP calls
- Provides actionable error messages per failure mode
- Exits with clear failure indication
- Doesn't require Claude to interpret raw tool output

**What "bad" looks like:**
```bash
curl -X POST "$API_URL/data" -d "$payload"
# Exits with curl's error code, no context
```

### Pacing Guidance

**Ask:** Is this skill used for tasks where quality/speed tradeoff matters?

**If yes, check:** Does it include explicit pacing guidance?

- Analysis/review tasks benefit from "prioritize accuracy over speed"
- High-volume processing benefits from "prioritize throughput, flag edge cases for manual review"

**Critique signal:** A skill that does careful analysis but says nothing about pacing may produce rushed output. A batch-processing skill that says nothing about throughput may over-analyze each item.

### Time-Sensitive Patterns

**Ask:** Does this skill reference APIs, libraries, or tools that change across versions?

**If yes, check:** Does it explicitly handle deprecated patterns? Are there version-specific instructions that could become outdated?

**Critique signal:** If a skill references specific API syntax without version context, flag the risk that training data may contain outdated patterns.

### Magic Numbers

**Ask:** Does this skill use numeric constants (timeouts, batch sizes, retry delays)?

**If yes, check:** Is the rationale documented? Could Claude or a future maintainer understand why the value was chosen?

**What "good" looks like:**

| Value | Setting | Rationale |
|-------|---------|-----------|
| 37s | API timeout | Server has 30s internal timeout + 7s network buffer |
| 128 | Batch size | Optimal for current rate limits (100 req/min + burst allowance) |

**What "bad" looks like:** `timeout = 37` with no explanation.

## Agent Architecture

Skills can spawn sub-agents via the Agent tool during execution. This carries real cost — context duplication, token overhead, latency — so the critic evaluates whether that cost is justified.

This section covers **bundled agents** (spawned by a skill as part of its workflow). It does not cover **standalone named agents** (definitions in `~/.claude/agents/` invoked directly by type) — those are their own artifacts, not part of a skill's design.

### The Orchestration Test

The single most important question: **does the parent do anything with the agent's output besides relay it?**

**Justified orchestration (parent earns its keep):**
- Spawns multiple agents, cross-references their outputs, synthesizes a verdict
- Evaluates agent output against criteria, branches on the result
- Transforms or filters agent output before presenting to user
- Retries or escalates based on agent failure modes

**Pass-through anti-pattern (parent is overhead):**
- Spawns one agent, receives output, relays to user verbatim
- Spawns one agent, does trivial formatting (adding a header), relays
- The "orchestrator" is just a prompt-forwarding layer

**What "good" looks like:** skill-critic itself — spawns defender + blind-tester in parallel, then cross-references their verdicts in Step 6 to decide which criticisms survive. The synthesis is real work neither agent could do alone.

**What "bad" looks like:** a skill that spawns a single research agent and returns its report unchanged. The skill adds ~1,500 words of instructions per invocation but produces identical output to invoking the agent directly.

### When Agents Are Justified

| Justification | Example |
|---|---|
| Parallel independent work | Multiple reviewers examining different dimensions simultaneously |
| Context isolation | Agent needs a clean slate — conversation history would bias its judgment |
| Model-tier optimization | Heavy lifting on opus, classification on sonnet |
| Adversarial independence | Two agents that must not see each other's work (blind comparison, steelman/critic) |

### When Agents Are Not Justified

| Pattern | Why it's overhead |
|---|---|
| Single agent, output relayed verbatim | Parent is a pass-through — collapse to single-agent |
| Agent does what the skill body could instruct directly | Skills already provide instruction isolation |
| Agent spawned "to keep context clean" with no other justification | Conversation contamination alone is not sufficient reason |

### Bundled vs. Named Custom Agents

Skills can use two kinds of agents. The choice affects maintainability, reusability, and token overhead.

A **bundled agent** is spawned during execution — its prompt lives in the skill's instructions or a reference file, launched with a generic `Agent()` call. A **named custom agent** has its own definition file in `~/.claude/agents/` and is invoked via `subagent_type`.

#### When to use which

**Use a bundled agent when:**
- The agent is a one-off helper specific to this skill's workflow
- It has no independent identity — invoking it outside this skill wouldn't make sense
- It doesn't need its own model, effort, or tools configuration
- The prompt is short enough to live inline without bloating the skill body

**Use a named custom agent when:**
- The agent has a distinct role with specific behavioral constraints (e.g., "only rate honestly, don't defend for the sake of defending")
- It could be invoked independently or reused by other skills
- It benefits from centralized config — model tier, effort level, tool allowlist, color
- It needs scope constraints that should be enforced by the agent definition, not by the caller's prompt

**Reference case:** skill-critic uses named agents (defender, blind-tester) because each has a specific role, behavioral constraints, model config, and could be invoked independently for ad-hoc skill testing.

#### Critique signals

**Duplication:** If a skill's bundled agent prompt closely mirrors an existing standalone agent definition, flag it. The skill should spawn the standalone by type rather than reinventing it.

**Promotion (bundled → named):** If a bundled agent has grown complex enough to have its own behavioral rules, model requirements, or potential for reuse, it should be promoted to a named agent definition.

**Demotion (named → bundled):** If a standalone agent only makes sense within one skill's workflow and nothing else invokes it independently, it probably belongs as a bundled agent in that skill's instructions instead.
