---
name: ideate
description: Structured thinking frameworks for strategy, decision-making, and reframing. 16 modes for creativity, analysis, and stress-testing. Not for coding tasks — for thinking through problems.
argument-hint: collide|state|lens|assume|pattern|bound|scaffold|simplify|invert|axiom|ripple|subtract|analog|constrain|timeshift|steelman
---

## Ideate

Apply domain-agnostic thinking frameworks to any problem. Each framework is a cognitive operation—a structured way to approach a specific type of challenge.

### Usage

```
/ideate <mode> [context]
/ideate <mode1>+<mode2> [context]
/ideate <mode1>+<mode2>+<mode3> [context]
/ideate [problem description]
```

**Solo** — single framework, unchanged behavior:

- `/ideate collide` — Force unexpected domain collisions
- `/ideate axiom "our pricing model"` — Rebuild from first principles

**Combination** — two or three modes, `+` separated:

- `/ideate axiom+invert "our pricing model"` — Rebuild, then stress-test
- `/ideate collide+steelman+lens "tutorial design"` — Generate, attack, synthesize

**Guided** — no mode specified, skill suggests based on triage:

- `/ideate "I need to rethink our pricing and stress-test it"`

If a mode isn't recognized, check aliases first. If no alias matches, treat the entire input as a problem description and fall through to guided mode.

### Framework Index

| Mode        | Aliases                      | Framework              | Use When...                                                         |
| ----------- | ---------------------------- | ---------------------- | ------------------------------------------------------------------- |
| `collide`   | `collision`, `recombine`     | Forced Recombination   | Stuck, need breakthrough ideas, conventional approaches exhausted   |
| `state`     | `mode`, `match`              | State-Task Matching    | Wrong energy for task, stuck in one mode, need to shift gears       |
| `lens`      | `perspectives`, `aggregate`  | Multi-Lens Synthesis   | Conflicting inputs, need to preserve disagreement productively      |
| `assume`    | `dig`, `critical`            | Assumption Archaeology | Blind spots, unchallenged beliefs, "the only way" thinking          |
| `pattern`   | `invariant`, `signal`        | Invariant Extraction   | Signal vs. noise, recurring themes, what persists across variations |
| `bound`     | `diverge`, `explore`         | Bounded Exploration    | Too rigid OR too unfocused, need calibrated wandering               |
| `scaffold`  | `symbol`, `stage`            | Symbolic Scaffolding   | Need structure, sequence, progression framework                     |
| `simplify`  | `cascade`, `upstream`        | Upstream Unification   | Too many interconnected problems, need 10x not 10% improvement      |
| `invert`    | `premortem`, `flip`          | Inversion              | Overconfident, need to stress-test, big commitment ahead            |
| `axiom`     | `firstprinciples`, `rebuild` | First Principles       | Iterating on inherited solutions, "everyone does it this way"       |
| `ripple`    | `secondorder`, `chain`       | Second-Order Effects   | Decision with unclear downstream consequences, incentive changes    |
| `subtract`  | `remove`, `vianegativa`      | Via Negativa           | Complexity creep, too many things, the answer might be "do less"    |
| `analog`    | `transfer`, `structural`     | Analogical Transfer    | Problem has a known structural shape, solved elsewhere              |
| `constrain` | `toggle`, `experiment`       | Constraint Play        | Analysis paralysis, unclear which constraints matter                |
| `timeshift` | `horizon`, `temporal`        | Temporal Shifting      | Trapped by urgency, unclear what matters long-term vs. short-term   |
| `steelman`  | `oppose`, `strongest`        | Steelmanning           | Dismissing opposition, need to stress-test your own position        |

### Intake Triage

When a user describes being stuck, use this dispatch to **suggest** an appropriate mode.

| Stuck Symptom                                                  | Suggested Mode | Why                                            |
| -------------------------------------------------------------- | -------------- | ---------------------------------------------- |
| Same thing implemented 5+ ways, growing special cases          | `simplify`     | Upstream cause eliminates variants             |
| Conventional solutions inadequate, need breakthrough           | `collide`      | Force unexpected recombinations                |
| Same issue recurring across contexts                           | `pattern`      | Extract the invariant signal                   |
| "Must be done this way", solution feels forced                 | `assume`       | Surface hidden constraints                     |
| Will it scale? Edge cases unclear?                             | `bound`        | Explore limits with calibrated wandering       |
| Conflicting advice/inputs                                      | `lens`         | Synthesize without flattening                  |
| Wrong energy, can't get started                                | `state`        | Match cognitive mode to task                   |
| Lack of structure, unclear sequence                            | `scaffold`     | Build symbolic progression                     |
| "I think this plan is solid" / overconfidence                  | `invert`       | Imagine failure to reveal blind spots          |
| "Everyone does it this way" / iterating on inherited approach  | `axiom`        | Rebuild from fundamental truths                |
| "What are the side effects?" / incentive or behavior change    | `ripple`       | Trace consequence chains forward               |
| "It's getting too complex" / adding things without simplifying | `subtract`     | Remove instead of add                          |
| "This feels like a known problem" / structural déjà vu         | `analog`       | Find solved instances of the same shape        |
| Too many options / unclear which constraints matter            | `constrain`    | Toggle constraints to find what's load-bearing |
| Everything feels urgent / can't prioritize                     | `timeshift`    | Shift time horizons to clarify importance      |
| "They just don't get it" / dismissing opposition               | `steelman`     | Build the strongest opposing case              |

> **Guided mode:** When no mode is specified, triage identifies the primary mode, then evaluates whether a combination would strengthen the output. Suggest the combination; don't auto-invoke. Load `references/combinations.md` for the catalog of sensible pairings.

> **Triage tiebreaker:** When multiple modes match, prefer the one whose role best fits what the user wants to do next — "I need new ideas" favors generative modes, "something keeps failing" favors adversarial, "I can't see the full picture" favors integrative.

### Framework References

When a mode is invoked, load the corresponding reference:

| Mode        | Reference                              |
| ----------- | -------------------------------------- |
| `collide`   | `references/forced-recombination.md`   |
| `state`     | `references/state-task-matching.md`    |
| `lens`      | `references/multi-lens-synthesis.md`   |
| `assume`    | `references/assumption-archaeology.md` |
| `pattern`   | `references/invariant-extraction.md`   |
| `bound`     | `references/bounded-exploration.md`    |
| `scaffold`  | `references/symbolic-scaffolding.md`   |
| `simplify`  | `references/upstream-unification.md`   |
| `invert`    | `references/inversion.md`              |
| `axiom`     | `references/first-principles.md`       |
| `ripple`    | `references/second-order-effects.md`   |
| `subtract`  | `references/via-negativa.md`           |
| `analog`    | `references/analogical-transfer.md`    |
| `constrain` | `references/constraint-play.md`        |
| `timeshift` | `references/temporal-shifting.md`      |
| `steelman`  | `references/steelmanning.md`           |

### Role Classification

Each mode belongs to a role based on its relationship to context. This determines how combinations execute.

| Role            | Modes                                                    | Context Relationship                   |
| --------------- | -------------------------------------------------------- | -------------------------------------- |
| **Meta**        | `state`                                                  | Routes to the right mode               |
| **Generative**  | `collide`, `axiom`, `scaffold`, `bound`, `analog`        | Commitment — no second-guessing        |
| **Adversarial** | `assume`, `invert`, `steelman`, `subtract`, `constrain`  | Fresh eyes — no investment in examined material |
| **Integrative** | `lens`, `pattern`, `ripple`, `simplify`, `timeshift`     | Full picture — sees everything         |

`state` is a dispatcher, not a framework — it does not appear in combinations. Run `/ideate state` first to identify the right mode, then invoke that mode.

### Combination Dispatch

When two or more modes are invoked together:

1) **Same role** (e.g., `axiom+scaffold`, `invert+subtract`) → Run in-context, sequential. No agents. Second step sees first step's output.
2) **Cross-role, two modes** (e.g., `axiom+invert`) → Ask the user: in-context (faster, you see the full chain and can participate) or independent agents (stronger independence, no contamination between roles)?
3) **Three modes** (e.g., `collide+steelman+lens`) → Always spawn agents. Each role runs independently; integrative agent sees all outputs.

**Defaults when asking:** If the problem is exploratory (brainstorming), suggest in-context. If evaluative (stress-testing a decision), suggest agents.

For execution details and agent prompt templates: load `references/orchestration.md`
For the full catalog of ~110 sensible combinations: load `references/combinations.md`

