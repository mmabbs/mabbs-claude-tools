# Criteria: Hooks

What makes something a hook (settings.json `"hooks"`, plugin `hooks/hooks.json`, or skill/agent frontmatter) rather than a rule, a skill, an agent, or a permission entry.

## What Earns Its Keep

A hook earns its keep when it provides at least one of four mechanical benefits:

1. **Guaranteed execution.** The harness fires hooks; the model can't forget, skip, or rationalize around them. This is the only config type with enforcement semantics — everything else (rules, CLAUDE.md, skills) is guidance the model follows with judgment and occasional drift.
2. **Event coupling.** ~30 lifecycle events cover the full session: tool calls (PreToolUse, PostToolUse, PostToolUseFailure), turns (UserPromptSubmit, Stop), sessions (SessionStart, SessionEnd), subagents, tasks, compaction, config changes, file watches (FileChanged), worktrees, and more. Nothing else in the config system can react to "a file changed on disk" or "Claude is about to stop."
3. **Power to intervene.** Hooks don't just observe — they block tool calls (`permissionDecision: deny`), rewrite tool inputs (`updatedInput`), block Claude from stopping (`decision: block`), inject context (`additionalContext`), and modify tool output. No other type can veto or alter the harness's behavior.
4. **Zero-context operation.** Hook logic runs outside the model — a shell script, HTTP call, or MCP tool costs no conversation tokens until it chooses to inject something. Async hooks run in the background without stalling the turn at all.

**The test:** "when Y happens, X must reliably occur" — where *reliably* matters more than *judgment*. If the sentence has no event ("when Y happens"), it's not a hook. If reliability doesn't matter, a rule is cheaper.

## What Disqualifies

1. **No triggering event.** Something invoked on demand, when a person or the model decides it's time, is a skill. Bolting a workflow onto UserPromptSubmit "so it always runs" turns every prompt into overhead.
2. **Needs full conversational judgment.** Hooks decide from narrow input — a tool call's JSON, a file path. Even `prompt` and `agent` handler types return a constrained yes/no verdict. If the decision needs the whole conversation's context, it belongs in a rule the model applies, not a hook.
3. **Drift is tolerable.** Style preferences, communication norms, soft conventions — a rule handles these for free. Hooks add per-event latency, a script to maintain, and a stripped-PATH environment to debug. Reserve them for guarantees.
4. **Heavy open-ended work in a blocking position.** A synchronous hook stalls the turn until it finishes (command hooks default to a 600s timeout). Long analysis or multi-step work belongs in an agent, or at minimum an `async: true` hook that reports back next turn.
5. **It's really a permission rule.** Static allow/deny of specific tools or commands is what settings.json `permissions` lists are for. A PreToolUse hook that just pattern-matches a tool name and denies reimplements permissions with more moving parts. Hooks earn the job only when the decision is conditional on the *input's content or external state*.

## Boundary Cases

### Hook vs. Rule

Enforcement vs. guidance. Both say "when X, do Y" — the rule version is read by the model and followed most of the time; the hook version is executed by the harness every time. The test: **what's the cost of one violation?** Annoyance → rule. Broken build, leaked secret, corrupted data → hook. The escalation signal: repeatedly strengthening a rule's wording ("NEVER", "ALWAYS", bold caps) because Claude keeps drifting means the instruction wants to be a hook.

**Intentional stacking is valid.** A hook and a rule (or CLAUDE.md section) covering the same instruction is not automatically redundancy. The rule teaches the model the *why* and shapes judgment; the hook catches the cases where the model drifts anyway. When evaluating overlap, test for **drift tolerance**: if the model ignores the rule, does the hook enforce it? If yes, the stacking is a compliance backstop, not dead weight. This is especially true at high-attention moments (SessionStart, UserPromptSubmit) where CLAUDE.md content competes with everything else for model attention.

### Hook vs. Skill

Trigger vs. invocation — the hook fires on an observed event; the skill is chosen. The hybrid case: hooks defined in a *skill's* frontmatter activate only while that skill runs (and support `once: true`). So "every time X happens *during this workflow*" doesn't need a global hook guarded by conditionals — it needs a skill-scoped hook.

### Hook vs. Agent

An `agent`-type hook spawns a subagent with read-only tools to verify a condition and return a verdict. That's still a hook: event-activated, verdict-shaped. The test: **is the output a decision about the event, or a work product?** "Did this edit break the naming convention? yes/no" → agent-type hook. "Review this diff and write up findings" → a real agent, invoked with judgment.

### Hook vs. Permission Entry

Both can stop a tool call. Permissions are declarative and static — allow/deny/ask lists matched on tool name and argument patterns. Hooks are programmable — they inspect the full input, consult files or external state, and can rewrite rather than just refuse. Start with permissions; graduate to a PreToolUse hook only when the decision needs logic.

### Multiple Hooks + Skills Serving One Workflow → Plugin

When a capability accretes components — a skill, two hooks, a helper script, maybe an agent — that all serve one workflow and only make sense together, that's a plugin candidate. The signal: enabling or disabling them only makes sense *as a set*, or you want the same set in another project without copy-paste. See criteria-plugins.md.

## Placement Discipline

Hooks live in four places with different lifetimes: user settings (all projects, always), project settings (this project, committed), plugin hooks.json (while the plugin is enabled), and skill/agent frontmatter (while the component is active). Place the hook at the narrowest scope that covers its purpose — a hook that only matters during one workflow does not belong in global settings. When auditing "what fires on event X," check all four locations; settings files alone are not the full picture.
