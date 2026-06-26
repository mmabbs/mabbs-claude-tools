# Constraint Play ("Experimental Constraints")

**Core operation:** Deliberately add or remove constraints to reveal which ones actually matter, which are self-imposed, and which are creative levers.

## Why It Works

We treat constraints as fixed when most are negotiable. By experimentally toggling constraints — removing real ones, adding artificial ones — you discover which constraints are *load-bearing* (the problem changes fundamentally without them) and which are *decorative* (the problem is the same without them). Artificial constraints can also force creativity: "What if we had to ship tomorrow?" produces different solutions than open-ended exploration.

## Process

1. **List all constraints** — Budget, time, tools, people, rules, conventions, assumptions
2. **Classify each** — Is this physics (immovable), policy (negotiable), or habit (self-imposed)?
3. **Remove one constraint** — "What if this didn't apply?" — Does the solution change?
4. **Add an artificial constraint** — "What if we also had to ___?" — Does it force a better idea?
5. **Identify the load-bearing constraints** — The ones that fundamentally shape the solution
6. **Focus only on those** — Everything else is negotiable

## Constraint Classification

| Type | Example | Movable? |
|------|---------|----------|
| **Physics** | Data can't travel faster than light | No |
| **Economics** | We have $X budget | Negotiable — can you change scope? |
| **Policy** | Company requires approval process | Negotiable — can you get an exception? |
| **Convention** | "We always use tool X" | Self-imposed — challenge it |
| **Assumption** | "Users won't pay for this" | Untested — validate it |

## Constraint Experiments

| Experiment | What It Reveals |
|------------|----------------|
| **Remove budget constraint** | Is the core idea sound, just under-resourced? |
| **Remove time constraint** | Are you cutting the wrong corners? |
| **Add "ship tomorrow" constraint** | What's the minimum viable version? |
| **Add "no code" constraint** | Can this be solved with process instead of engineering? |
| **Remove tool constraint** | Are you limiting solutions to what your current tools support? |
| **Add "explain to a child" constraint** | Is the concept too complex, or just poorly communicated? |

## Applications

| Context | Constraint Play |
|---------|----------------|
| **Product** | "What if we had 10x users tomorrow? What breaks first?" |
| **Process** | "What if this meeting didn't exist? What would we lose?" |
| **Career** | "What if money weren't a factor? What would I do?" |
| **Design** | "What if we could only use one screen/page/button?" |
| **Writing** | "What if this had to be half the length?" |

## Red Flags You Need This

- Analysis paralysis — too many options, no forcing function
- "We can't because..." repeated without testing whether it's true
- Scope creep — no clear boundaries on what's in and out
- The solution feels over-engineered — unclear which constraints it's actually solving for
- "What if..." questions keep coming up but aren't being systematically explored

## Constraint Prompts

- "Which of these constraints would I remove if I could only remove one?"
- "What constraint, if added, would make the decision obvious?"
- "Is this constraint real or inherited?"
- "What would we build if we started today with no existing system?"
- "What's the tightest constraint that still produces a good outcome?"

## Distinction from `bound`

`bound` (Bounded Exploration) calibrates your **exploration scope** — how wide to wander before converging. `constrain` changes the **problem definition itself** by toggling constraints on and off. `bound` is about managing your search process; `constrain` is about reshaping the problem you're searching within.

## Remember

- Most constraints are softer than they appear — test them
- Artificial constraints are creative tools, not limitations
- The constraint you'd most hate to remove is probably the most important one
- Pair with `axiom` to separate fundamental constraints from conventional ones
- "What's the tightest constraint that still works?" is often the most useful question
