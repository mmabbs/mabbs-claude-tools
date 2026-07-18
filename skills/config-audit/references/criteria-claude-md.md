# Criteria: CLAUDE.md

What makes something CLAUDE.md content (`~/.claude/CLAUDE.md`, project `CLAUDE.md` / `.claude/CLAUDE.md`, `CLAUDE.local.md`) rather than a rule, a memory, a skill, or documentation.

## What Earns Its Keep

CLAUDE.md earns its keep when content needs one of four mechanical properties:

1. **Unconditional presence.** Every CLAUDE.md in scope loads fully at session start, every conversation, no invocation and no path match required. It is the only "Claude always knows this from turn one" guarantee (unscoped rules share the mechanics — the boundary below decides placement).
2. **Layered concatenation.** Global (`~/.claude/CLAUDE.md`) → project → `CLAUDE.local.md`, walking up the directory tree from CWD, all concatenated with closer files read last. Personal baseline, team baseline, and per-machine overrides compose without editing each other. `@path` imports (max 4 hops) pull in shared files at load time.
3. **Team distribution.** The project file is checked in — the one config type both humans and Claude read, and the default place a collaborator (or future you) looks to understand how Claude is set up here.
4. **Nested lazy loading.** A `CLAUDE.md` in a subdirectory loads only when Claude reads files there — startup-free orientation for monorepo sub-areas.

**The test:** would *any* conversation in this project go wrong without this line? CLAUDE.md is the orientation document — what the project is, how it's laid out, where key things live, which mode to operate in. If the line only matters for some files, some workflows, or some tasks, it belongs in a scoped type instead.

## What Disqualifies

1. **Derivable from the codebase.** Structure, conventions, and APIs Claude can read fresh — the `/doctor` check now flags exactly this for trimming. Every derivable line is pure tax.
2. **Path-specific instructions.** "In `src/components/`, always use..." pays always-on tokens for sometimes-relevant guidance. That's a rule with `paths:`.
3. **Procedures.** Multi-step workflows invoked occasionally are skills — progressive disclosure exists so procedures don't ride along in every conversation.
4. **User-specific context in a project file.** The project CLAUDE.md is team-visible and project-scoped. Who the user is, their preferences, feedback history — that's memory (Claude-only) or the global CLAUDE.md (personal, all projects).
5. **Reference material.** Long tables, API docs, exhaustive listings. Adherence degrades as the file grows (the "too long" warning exists for a reason); reference content belongs in supporting docs Claude reads on demand, or skill reference files.
6. **Session-scoped facts.** Current debugging state, in-progress work — that's conversation, or at most a task note.

## Boundary Cases

### CLAUDE.md vs. Rules

Mechanically near-identical for unscoped content — both load fully at startup. The test: **orientation or policy?** What the project *is* (identity, layout, key files, learning mode) → CLAUDE.md, the map read first. How Claude must *behave* (conventions, prohibitions, standing instructions) → rules, which are modular, independently retirable, symlinkable across projects, and — the decisive case — scopable with `paths:` the moment they stop being universal. When an instruction could ever be scoped or shared, put it in a rule now rather than migrating it later.

### CLAUDE.md vs. Memory

Team-visible project truth vs. Claude-only user context. If anyone working on the project should know it → CLAUDE.md. If it's about the user, their preferences, or how Claude should work with them specifically → memory. (Same test as in criteria-memory.md, from the other side.)

### CLAUDE.md vs. README

Audience. README documents the project for humans; CLAUDE.md instructs Claude. Don't duplicate the README into CLAUDE.md — Claude can read the README, and `@README.md` imports it wholesale if it's genuinely always needed. CLAUDE.md should hold only what the README wouldn't say: operating instructions, constraints, pointers.

### Global CLAUDE.md vs. Project CLAUDE.md

Same file type, different blast radius. Global content loads in *every* project — a line that assumes one project's context becomes noise (or misdirection) everywhere else. Personal, project-independent defaults → global. Anything that names a specific project's files, tools, or conventions → that project's file.

## Length Discipline

CLAUDE.md is the most expensive real estate in the config system: every line costs tokens in every conversation and competes for adherence with every other line. The guidance target is under ~200 lines. The cheapest wins, in order: delete derivable content, move path-specific content to scoped rules, move procedures to skills, move reference material to on-demand docs. Splitting into @-imports organizes the file but does *not* reduce cost — imports load at startup too. Block-level HTML comments are stripped before injection, so annotations for human editors are free.
