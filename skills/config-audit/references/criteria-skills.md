# Criteria: Skills

What makes something a skill (`~/.claude/skills/<name>/SKILL.md`, `.claude/skills/`) rather than a rule, a hook, an agent definition, or just a good prompt.

## What Earns Its Keep

A skill earns its keep when it provides at least one of five mechanical benefits:

1. **Progressive disclosure** — only the name and description (capped at 1,536 chars) load at session start; the full body loads on invocation. A skill can hold a 400-line procedure that costs ~50 tokens of standing context. Rules and CLAUDE.md pay full price up front.
2. **Dual invocation with control** — invocable by the user (`/name`) and by the model (matched on description), with each channel independently switchable: `disable-model-invocation: true` for user-only, `user-invocable: false` for model-only background knowledge.
3. **Arguments and dynamic context** — `$ARGUMENTS`, positional `$0`/`$1`, named arguments from frontmatter, plus `` !`command` `` preprocessing that runs shell commands and injects their output before Claude sees the content. A rule can't parameterize; a hook can't take user arguments.
4. **Supporting files** — references, templates, and scripts live in the skill directory, loaded or executed only when the skill body links to them. Second layer of progressive disclosure.
5. **Per-invocation overrides** — `model`, `effort`, `allowed-tools`, `disallowed-tools` apply for the skill's turn, and `context: fork` + `agent:` can push the whole thing into an isolated subagent. Scoped `hooks` in frontmatter fire only while the skill is active.

**The test:** is this a repeatable procedure that someone — user or model — *chooses to run*, whose instructions shouldn't cost context until that moment? If it must apply always, it's a rule or CLAUDE.md. If it must fire on an event, it's a hook.

## What Disqualifies

1. **Always-on behavior.** If Claude must follow it in every conversation regardless of invocation, progressive disclosure is a bug, not a feature — the instruction would routinely not be loaded when needed. That's a rule or CLAUDE.md.
2. **Must fire deterministically on an event.** "Every time a file is written, lint it" can't rely on the model choosing to invoke a skill. That's a hook.
3. **Pure facts with no procedure.** Context about the user or project with no steps to execute is a memory (user-specific) or CLAUDE.md/rule (project-wide).
4. **One-off task.** A procedure used once is a prompt. Skills are infrastructure — they pay off across sessions.
5. **The value is the execution environment, not the instructions.** If what you actually need is a pinned model, restricted tools, and a persistent system prompt reused across many differently-shaped tasks, that's an agent definition. A skill's `context: fork` borrows an agent's environment for one procedure; it doesn't replace the agent.
6. **Body over ~500 lines.** Everything in an invoked skill stays in context for the rest of the session. Oversized bodies belong in supporting files, loaded selectively.

## Boundary Cases

### Skill vs. Hook

Activation is the test: **an event or a decision?** Hooks fire when the harness observes a trigger (tool call, session start, file change) — no one decides. Skills activate when the user types `/name` or the model judges the description relevant. Don't be misled by hooks' `prompt` and `agent` handler types — those put judgment in the *handler* (a yes/no verdict on narrow input), but activation is still the trigger. Also note the hybrid: a skill's frontmatter can carry hooks that exist only while the skill is active — event-automation scoped to a chosen workflow.

### Skill vs. Agent

The old test ("does it need its own context, model, tools? → agent") is obsolete: `context: fork`, `agent:`, `model`, and `allowed-tools` give skills all of that per-invocation. The current test: **is the reusable asset the instructions or the executor?** A skill packages a *procedure* — one workflow, possibly forked into a subagent to run. An agent packages a *worker* — system prompt, model, tool policy — that many different briefs get dispatched to. If you'd send it varied tasks, it's an agent; if it does one thing when called, it's a skill.

### Skill vs. Rule

Procedure vs. policy. Steps, tools, and an output → skill. A constraint on how all work is done → rule. Both accept `paths:` frontmatter, so path-scoping doesn't distinguish them — a path-scoped *skill* auto-loads a procedure when relevant files are read; a path-scoped *rule* auto-loads a constraint.

### Skill vs. Command (legacy)

Same slash-command surface; skills supersede. A skill adds the directory (supporting files), invocation-control frontmatter, and model auto-invocation. On a name conflict, the skill wins. Don't create new `commands/` files; migrate a command to a skill when it needs any of the above, otherwise leave it working.

### Skill vs. Memory

A memory informs judgment with facts; a skill directs execution with steps. "The user prefers numbered lists" is memory. "How to format a session note" is a skill. If a memory has grown a step-by-step procedure inside it, the procedure wants to be a skill.

## Description Discipline

The description is the skill's entire standing presence — it's what the model matches against when deciding to auto-invoke, within the 1,536-char cap (shared with `when_to_use`). A skill that never triggers usually has a description problem, not a body problem: state what it does *and* the situations that should trigger it, in the vocabulary a user would actually use.
