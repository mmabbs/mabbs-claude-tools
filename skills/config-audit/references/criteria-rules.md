# Criteria: Rules Files

What makes something a rule file (`~/.claude/rules/`, `.claude/rules/`) rather than CLAUDE.md content, a memory, a skill, or a hook.

## What Earns Its Keep

A rule file earns its keep when it provides at least one of four mechanical benefits:

1. **Conditional loading via `paths:`** — a rule with `paths:` frontmatter loads only when Claude reads files matching the glob, not at startup. This is the only way to make a standing instruction cost zero tokens until it's relevant. CLAUDE.md can't do this; every line of it taxes every conversation.
2. **Modularity** — one concern per file, discovered recursively (subdirectories work), each independently editable, archivable, and auditable. A 40-line rule file is maintainable; the same content as CLAUDE.md section #14 is not.
3. **Cross-project sharing via symlinks** — symlink a shared standards file into multiple projects' `rules/` directories. Edit once, applies everywhere. CLAUDE.md content would have to be duplicated or @-imported with absolute paths.
4. **Scope layering** — user-level rules (`~/.claude/rules/`) load before project rules, so project rules effectively win. This gives you a personal baseline that individual projects can override without editing the global file.

**The test:** is this a standing behavioral instruction Claude must follow without being asked — and does it either apply only to part of the codebase (scope it with `paths:`), cover one separable concern (modularity), or need to exist in multiple projects (symlink)? If it's behavioral but none of those apply, it still qualifies — unscoped rules and CLAUDE.md are mechanically equivalent at startup — but the boundary with CLAUDE.md decides placement (below).

## What Disqualifies

1. **Describes context instead of prescribing behavior.** "The deploy pipeline runs on Fridays" is a memory or CLAUDE.md fact. Rules start with "Don't...", "Always...", "When X, do Y."
2. **Derivable from the codebase.** Conventions Claude can read fresh from the code don't need a rule restating them — same logic as the `/doctor` check that flags derivable CLAUDE.md content.
3. **Must be enforced, not just followed.** Rules are guidance — Claude reads them and can still drift, especially in long sessions. If violation is unacceptable (never touch `.env`, always run the formatter), that's a hook or a permission rule, which the harness enforces deterministically.
4. **A procedure someone triggers.** Multi-step workflows invoked on demand ("do a release", "write a session note") are skills. A rule that's really a recipe wastes always-on context on something used occasionally.
5. **One-off or session-scoped.** "For this refactor, keep the old API" is a conversation instruction, not infrastructure.
6. **Duplicates CLAUDE.md.** Same instruction in both places doubles the token cost and guarantees drift when one gets edited.
7. **Project orientation.** What the project *is*, its layout, its key files — that's CLAUDE.md's job. Rules assume orientation already happened.

## Boundary Cases

### Rule vs. CLAUDE.md

Unscoped rules and CLAUDE.md both load fully at startup — the mechanical difference only appears with `paths:`. The test: **could this instruction ever be scoped, shared, or retired independently?** Path-specific → rule with `paths:`, always. Separable standing concern (git conventions, testing policy) → rule, for modularity. Project identity, layout, orientation → CLAUDE.md. Short universal pointers ("changelog lives at X") → CLAUDE.md is fine; don't create a five-line rule file for one fact.

### Rule vs. Memory

**Rules prescribe behavior. Memories describe context.** Imperative voice ("Don't...", "Always...") signals rule; declarative facts about the user, projects, or resources signal memory. When fuzzy, prefer memory — a misplaced memory is low-cost (Claude applies judgment), while a misplaced rule adds to the instruction surface Claude must obey, and rules accumulate faster than they get cleaned up. Graduate a memory to a rule only when the instruction is genuinely behavioral and session-independent — something Claude must do the same way every time.

### Rule vs. Skill

A rule is a standing constraint; a skill is an on-demand procedure. Note that skills also accept `paths:` frontmatter now, so path-triggered loading alone doesn't decide it. The test: **is it policy or procedure?** "Never use `any` in this directory" constrains everything Claude does there → rule. "Here's the 8-step process for adding a migration" is a workflow with steps and tools → skill, which stays out of context until invoked.

### Rule vs. Hook

Both automate behavior; the difference is who executes. A rule is read by the model and followed with judgment — and occasionally forgotten. A hook is executed by the harness and cannot be skipped. The test: **is drift tolerable?** Style preferences, communication norms, soft conventions → rule. Guarantees ("must never", "must always") → hook. If you find yourself strengthening a rule's wording because Claude keeps ignoring it, that's the signal it wants to be a hook.

## Scoping Discipline

`paths:` is the rule system's main mechanical advantage — use it. Every unscoped rule is a permanent tax on every conversation in scope. When writing a new rule, the first question is "what files does this actually apply to?" — only leave it unscoped when the honest answer is "all of them." Globs support brace expansion (`src/**/*.{ts,tsx}`) and match through symlinked paths.
