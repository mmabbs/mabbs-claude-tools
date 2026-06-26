## Ideate

> **Requires Opus.** This skill is reasoning-intensive — frameworks need to hold a problem's full structure, commit to a cognitive disposition, and produce output that survives adversarial scrutiny. Lower-tier models produce shallow results that defeat the purpose. Solo modes technically function on Sonnet but expect degraded quality; combinations and agent pipelines require Opus.

Structured thinking frameworks for Claude Code. Sixteen cognitive operations — covering creativity, analysis, and reframing — each accessible as a mode you invoke when you're stuck on a specific type of problem.

Instead of generic "brainstorm this" prompts, Ideate gives Claude a concrete framework to apply: a defined process, diagnostic questions, and domain-specific examples. Each mode targets a different kind of stuck — wrong energy, blind spots, complexity creep, overconfidence — and the skill can suggest which mode fits when you describe the problem.

**This is a thinking skill, not a coding skill.** It has no relation to debugging, code review, or implementation tasks. If you want to think through a coding *project* — where to start, how to architect, which tradeoffs matter — that's strategy, and Ideate handles it. But it won't help you find bugs or write code.

### What It Does

1) **Solo mode** — Invoke one framework directly. Claude loads the reference and applies it step-by-step to your problem.
2) **Combination mode** — Chain two or three frameworks with `+`. Same-role combos run sequentially; cross-role combos can run as independent agents for stronger independence between steps.
3) **Guided mode** — Describe what you're stuck on without specifying a mode. The skill triages your problem and suggests an appropriate framework (or combination).

### The 16 Modes

| Mode | Framework | Use When... |
|---|---|---|
| `collide` | Forced Recombination | Stuck, need breakthrough ideas, conventional approaches exhausted |
| `state` | State-Task Matching | Wrong energy for task, stuck in one mode, need to shift gears |
| `lens` | Multi-Lens Synthesis | Conflicting inputs, need to preserve disagreement productively |
| `assume` | Assumption Archaeology | Blind spots, unchallenged beliefs, "the only way" thinking |
| `pattern` | Invariant Extraction | Signal vs. noise, recurring themes, what persists across variations |
| `bound` | Bounded Exploration | Too rigid OR too unfocused, need calibrated wandering |
| `scaffold` | Symbolic Scaffolding | Need structure, sequence, progression framework |
| `simplify` | Upstream Unification | Too many interconnected problems, need 10x not 10% improvement |
| `invert` | Inversion | Overconfident, need to stress-test, big commitment ahead |
| `axiom` | First Principles | Iterating on inherited solutions, "everyone does it this way" |
| `ripple` | Second-Order Effects | Decision with unclear downstream consequences |
| `subtract` | Via Negativa | Complexity creep, the answer might be "do less" |
| `analog` | Analogical Transfer | Problem has a known structural shape, solved elsewhere |
| `constrain` | Constraint Play | Analysis paralysis, unclear which constraints matter |
| `timeshift` | Temporal Shifting | Trapped by urgency, unclear what matters long-term |
| `steelman` | Steelmanning | Dismissing opposition, need to stress-test your own position |

### Usage

```
/ideate collide                          # Solo: force unexpected domain collisions
/ideate axiom "our pricing model"        # Solo with context
/ideate axiom+invert "our pricing model" # Combination: rebuild, then stress-test
/ideate "I need to rethink our pricing"  # Guided: skill suggests the mode
```

### Sample Output

**Input:** `/ideate invert "launching our indie game in Early Access"`

**Output (abbreviated):**

> **Inversion: How could we guarantee this Early Access launch fails?**
> 
> 1) **Ship with no content roadmap** — Players tolerate EA bugs but not silence. A launch with no visible plan for what's next signals abandonment.
> 2) **Ignore the first 48 hours of feedback** — The EA audience self-selects for people who want to shape the game. Ignoring them in the critical window burns your most invested players.
> 3) **Price it like a finished game** — $30 for an incomplete experience sets the wrong expectation. Every missing feature becomes a betrayal, not a known gap.
> 
> **Safeguards:**
> - Publish a 3-month roadmap before launch day
> - Dedicate a team member to community response for the first week
> - Price 30-40% below target 1.0 price with a visible "EA discount" label
> 
> *Each failure mode is now a checklist item. The pre-mortem is more honest than the post-mortem — hindsight bias hasn't kicked in yet.*

### Requirements

| Dependency | Required? | Without it |
|---|---|---|
| Claude Code | Yes | The skill runs inside Claude Code's skill system |
| Opus model | Yes | Frameworks produce shallow, generic output on lower-tier models; combinations and pipelines are not recommended without Opus |
| Agent tool | For combinations | Solo modes work without it; cross-role combos and three-mode pipelines use agents for independence between frameworks |

No external tools, APIs, or plugins needed.

> **Tip — effort:** These frameworks are reasoning-heavy. For best results, raise the session effort to `high`, `xhigh`, or `max` (e.g. `/effort max`) before invoking — especially for combinations, where multiple frameworks run in sequence or across agents. Note: `xhigh` is only available on Opus 4.8+; Opus 4.6 supports `high` and `max`.

### Installation

```bash
# Clone and copy
git clone --depth 1 https://github.com/mmabbs/mabbs-claude-skills.git
cp -r mabbs-claude-skills/skills/ideate ~/.claude/skills/

# Or for project-scoped installation
cp -r mabbs-claude-skills/skills/ideate .claude/skills/
```

Claude Code detects new skills without a restart.

### Combinations

Modes are classified into roles that determine how combinations execute:

| Role | Modes | Relationship to Context |
|---|---|---|
| **Meta** | `state` | Routes to the right mode (doesn't combine) |
| **Generative** | `collide`, `axiom`, `scaffold`, `bound`, `analog` | Builds forward with commitment |
| **Adversarial** | `assume`, `invert`, `steelman`, `subtract`, `constrain` | Examines with fresh eyes |
| **Integrative** | `lens`, `pattern`, `ripple`, `simplify`, `timeshift` | Sees the full picture |

- **Same role** (e.g., `axiom+scaffold`) — runs sequentially in-context
- **Cross-role, two modes** (e.g., `axiom+invert`) — asks your preference: in-context or independent agents
- **Three modes** (e.g., `collide+steelman+lens`) — always spawns agents for independence

The `references/combinations.md` file catalogs ~110 sensible pairings with rationale and examples. The catalog is only loaded when a combination or guided-mode request is made — solo mode invocations don't touch it.

### Bundled Files

| File | Purpose |
|---|---|
| `SKILL.md` | Skill definition — framework index, intake triage, dispatch logic |
| `references/orchestration.md` | How combinations execute — role dispositions, agent templates, output conventions |
| `references/combinations.md` | Catalog of ~110 mode combinations with rationale and examples |
| `references/domain-agnostic-thinking-skills.md` | Conceptual overview — all sixteen operations in condensed form; the first eight are adapted from MonadFramework, the rest are original extensions |
| `references/forced-recombination.md` | `collide` framework reference |
| `references/state-task-matching.md` | `state` framework reference |
| `references/multi-lens-synthesis.md` | `lens` framework reference |
| `references/assumption-archaeology.md` | `assume` framework reference |
| `references/invariant-extraction.md` | `pattern` framework reference |
| `references/bounded-exploration.md` | `bound` framework reference |
| `references/symbolic-scaffolding.md` | `scaffold` framework reference |
| `references/upstream-unification.md` | `simplify` framework reference |
| `references/inversion.md` | `invert` framework reference |
| `references/first-principles.md` | `axiom` framework reference |
| `references/second-order-effects.md` | `ripple` framework reference |
| `references/via-negativa.md` | `subtract` framework reference |
| `references/analogical-transfer.md` | `analog` framework reference |
| `references/constraint-play.md` | `constrain` framework reference |
| `references/temporal-shifting.md` | `timeshift` framework reference |
| `references/steelmanning.md` | `steelman` framework reference |

### Acknowledgments & Provenance

The first eight modes — `collide`, `state`, `lens`, `assume`, `pattern`, `bound`, `scaffold`, `simplify` — are a remix and substantial reworking of ideation-framework skills originally published by GitHub user **agentgptsmith** in `MonadFramework/.claude/skills` ([github.com/agentgptsmith/MonadFramework](https://github.com/agentgptsmith/MonadFramework) — repository deleted; confirmed unavailable June 2026). The original is no longer available and was not captured under a known license.

**What's mine vs. theirs:** the taxonomy and core framing of those eight modes derive from the original. The other eight modes (`invert`, `axiom`, `ripple`, `subtract`, `analog`, `constrain`, `timeshift`, `steelman`), all framework prompts and references, the role-based combination system, the orchestration logic, and the intake triage are newly authored or substantially rewritten by me. Domain-agnostic write-ups of all sixteen live in `references/domain-agnostic-thinking-skills.md`. Errors and changes are my own.

If the original author objects to this attribution or to republication of the derived material, contact me and I'll comply. See the repository [`NOTICE`](../../NOTICE) for how licensing is scoped around this third-party material.
