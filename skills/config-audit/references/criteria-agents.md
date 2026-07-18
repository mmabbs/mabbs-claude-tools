# Criteria: Agent Definitions

What makes something an agent (`~/.claude/agents/*.md`) rather than a skill, workflow, or good briefing habit.

## What Earns Its Keep

An agent definition earns its keep when it provides at least one of five mechanical benefits that a bare `Agent()` call can't:

1. **Model pinning** — hardcode Sonnet for lookups, Opus for synthesis. Without a definition, every subagent inherits the session model, paying top-tier rates for simple work.
2. **Persistent system prompt** — bake in instructions, constraints, and output format once. Without a definition, the orchestrator rewrites the full brief every invocation, spending tokens and risking drift.
3. **Tool restrictions** — limit what the agent can touch. A research agent that can't write files. A reviewer that can't edit code.
4. **Skill preloading** — pre-load specific skills into context at startup so the agent doesn't need to discover them mid-task.
5. **Scoped permissions** — set permission mode per agent (e.g., auto-approve edits for a formatter).

**The test:** if a pattern wouldn't benefit from any of these five, it's not worth a definition file. It might be a skill, a workflow component, or just a better orchestrator prompt.

## What Disqualifies

- **No mechanical benefit.** The "agent" is really just a well-structured prompt passed to a generic subagent. A good brief doesn't need a definition file.
- **One-off task.** The pattern appeared once and is unlikely to recur. Definitions are infrastructure — they pay off across sessions.
- **Heavy iteration needed.** If the task requires frequent course corrections and back-and-forth with the user, it belongs in the main conversation, not a fire-and-forget subagent.
- **Trivial overhead.** Quick, targeted work where subagent startup cost exceeds the benefit of isolation.

## Boundary Cases

### Agent vs. Skill

Skills can now fork into subagents with pinned models (`context: fork`, `agent:`, `model` frontmatter), so the old "own context vs. current context" test no longer distinguishes them. The real test: **is the reusable asset the instructions or the worker?**

- **Skill** — the asset is a set of instructions. The skill defines *what to do* and can be invoked by the user, the orchestrator, or even a hook. It may spawn its own subagent internally, but the skill file is the entry point.
- **Agent** — the asset is a configured worker. The definition pins a model, restricts tools, and bakes in a system prompt so the orchestrator can spawn it by name without briefing it each time.

If the value is "a reusable procedure that might run in different contexts" → skill. If the value is "a pre-configured worker the orchestrator dispatches for a known task shape" → agent.

### Agent vs. Workflow Component

If the coordination between multiple agents is mechanical — loops, conditionals, fan-outs, dedup, counting — the agents might be better as components in a Workflow script. Agents handle reasoning; the Workflow script handles logistics. Signal: you'd describe the coordination as "for each X, do Y, then merge and filter" rather than "figure out what to do next."

### Agent vs. Briefing Habit

If the orchestrator could achieve the same result by writing a slightly better prompt to a generic subagent, there's no agent here — just a briefing pattern worth remembering (possibly as a memory file or a note in CLAUDE.md).

### Agent vs. Hook

The distinction is **activation**, not capability. Hooks can carry model-backed handlers (`prompt`/`agent` handler types), so both can involve judgment. What separates them: a hook fires on a lifecycle event (PreToolUse, SessionEnd, etc.); an agent is dispatched by a decision. If the trigger is "whenever X happens" → hook. If the trigger is "the orchestrator decided this task needs a worker" → agent.

## Qualification Threshold

A session pattern graduates to an agent candidate when it scores on **two or more** of three lenses:

1. **Repetition** — the same structural pattern (same tool sequence, same output shape, same constraints) appeared multiple times across sessions.
2. **Context cost** — the work filled significant main-context space when a subagent could have done it and returned a summary.
3. **Efficiency gap** — a baked-in system prompt would have prevented repeated briefing, model misrouting, or coordination overhead.

Repetition alone isn't enough if the work was fast and cheap. Context cost + efficiency gap qualifies even for a pattern that appeared once.

## Deployment Patterns

When recommending an agent, specify which pattern fits:

- **Solo (fire-and-forget)** — self-contained task, return summary, terminate. Research, extraction, validation, code search.
- **Parallelized** — same agent spawned N times on different inputs. Multi-source research, batch processing.
- **Agent Team member** — when findings from one worker should change what another does. Signals: competing hypotheses, iterative design, dynamic task discovery, cross-domain synthesis.
- **Workflow component** — when coordination is mechanical and belongs in a script, not in prompts.
