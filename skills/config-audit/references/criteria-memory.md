# Criteria: Memory Files

What makes something a memory file (`~/.claude/projects/<project>/memory/`) rather than a rule, CLAUDE.md content, or something that shouldn't be persisted at all.

## What Earns Its Keep

Memory files store information that is:

1. **Useful across future conversations** — not just this session
2. **Not derivable from the current project state** — can't be read fresh from code, config, or git
3. **About the user, their feedback, their projects, or their external resources** — not about how Claude should behave (that's a rule)

The four memory types and what each captures:

- **User** — role, goals, expertise, preferences. Helps Claude tailor future interactions to who the user actually is.
- **Feedback** — corrections AND validations of Claude's approach. What to avoid, what worked. Includes the *why* so edge cases can be judged.
- **Project** — ongoing work context not in code or git: who's doing what, why, deadlines, decisions. Decays fast — the *why* helps future Claude judge whether it's still relevant.
- **Reference** — pointers to external resources and their purpose. Where to find things outside the project directory.

## What Disqualifies (Red Flags)

These are things that *look* like memories but shouldn't be stored as such. If a candidate trips any of these, it doesn't belong in memory:

1. **Derivable from code** — file paths, project structure, architecture, conventions that can be read fresh from the codebase.
2. **Derivable from git** — commit history, recent changes, who changed what.
3. **The fix itself** — a bug fix or solution already captured in code and commit messages.
4. **Ephemeral** — current debugging state, in-progress work, things true only for this session.
5. **Rapidly decaying** — facts with a shelf life of hours to days (deploy status, PR state, version-pinned details).
6. **Already documented** — covered by CLAUDE.md, project rules, or config files.
7. **Generic knowledge** — baseline competencies that wouldn't change Claude's behavior.
8. **Unverified** — speculation or guesses not confirmed by evidence.
9. **Summary of source** — a lossy snapshot of something that should be read fresh from its source.

## Boundary Cases

### Memory vs. Rule

**Rules prescribe behavior. Memories describe context.**

A memory that starts with "Don't...", "Always...", or "When X, do Y" is almost certainly a rule. Memory files should inform Claude's judgment — not direct it with imperative instructions.

However: Claude has poor agentic steering on what should be a memory vs. a rule, and this skill defaults to fewer rules rather than more. The reasoning agent should have a **high bar** for recommending something move from memory to rule. Only recommend it when the instruction is genuinely behavioral and session-independent — something Claude must do the same way every time regardless of context.

If the boundary is fuzzy, prefer memory. A misplaced memory is low-cost (Claude reads it and applies judgment). A misplaced rule adds to the instruction surface Claude must obey, and rules accumulate faster than they get cleaned up.

### Memory vs. CLAUDE.md

CLAUDE.md is project-scoped, version-controlled, and visible to anyone working on the project. Memory is user-specific, auto-loaded, and cross-session.

- If the information is about a project and anyone working on it should know → CLAUDE.md
- If the information is about the user, their preferences, or how Claude should work with them specifically → memory
- If the information is project context that only matters for Claude interactions (not human collaborators) → memory is fine, but CLAUDE.md is also valid if it's stable enough

### Memory vs. Nothing

The hardest call. Not everything learned in a session needs to be remembered. The test: **would a future Claude session produce meaningfully worse output without this information?** If the answer is "it would figure it out from context," don't store it.

### Memory Staleness

Memory records are claims about what was true *when written*. Before acting on a memory that names a specific file, function, flag, or project state:

- If it names a file path: check the file exists
- If it names a function or flag: grep for it
- If the user is about to act on the recommendation: verify first

"The memory says X exists" is not evidence that X exists now.

## Index Discipline

`MEMORY.md` is an index, not a memory. Each entry is one line under ~150 characters. The content lives in the individual memory files. Lines after 200 in MEMORY.md are truncated from context, so the index must stay concise.
