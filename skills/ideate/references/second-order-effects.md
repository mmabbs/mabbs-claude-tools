# Second-Order Effects ("Ripple Mapping")

**Core operation:** Trace consequence chains 2-3 steps forward. Most decisions are optimized for first-order effects; the surprises live in second- and third-order consequences.

## Why It Works

First-order thinking asks: "What happens if I do X?" Second-order thinking asks: "And then what? And then what after *that*?" Systems are interconnected — pulling one lever moves others. The people who consistently make good long-term decisions are the ones who think in chains, not snapshots.

## Process

1. **State the decision or change** — What are you about to do?
2. **Map first-order effects** — The obvious, immediate consequences
3. **For each first-order effect, ask "and then what?"** — Map the second-order consequences
4. **Repeat once more** — Third-order effects (diminishing certainty, but high value)
5. **Flag surprises** — Which downstream effects weren't obvious from the original decision?
6. **Decide** — Do the downstream consequences change your plan?

## The Chain Template

```
Decision: _______________

1st order: [obvious effect]
  2nd order: [consequence of that effect]
    3rd order: [consequence of the consequence]

1st order: [another obvious effect]
  2nd order: ...
    3rd order: ...
```

## Applications

| Context | Ripple Question |
|---------|----------------|
| **Policy change** | "If we change this rule, how do people adapt? And then what?" |
| **Feature addition** | "If users get this feature, what behavior changes? What do they stop doing?" |
| **Hiring** | "If we hire for X, what does the team dynamic become? What does that cause?" |
| **Price change** | "If we lower the price, who new comes in? How does that change the community?" |
| **Architecture** | "If we add this dependency, what maintenance burden follows? What does that block?" |

## Red Flags You Need This

- Making a decision with obvious short-term benefits and unclear long-term effects
- "What are the side effects of this?"
- A change that affects incentive structures (pricing, rewards, penalties)
- Introducing something that will change user/team behavior
- Architectural decisions that create irreversible dependencies

## Ripple Prompts

- "And then what?"
- "Who adapts to this change, and how?"
- "What does this make easier? What does it make harder?"
- "If this works perfectly, what new problem does it create?"
- "What feedback loop does this create or break?"

## Common Ripple Patterns

| Pattern | Example |
|---------|---------|
| **Incentive shift** | Free tier attracts users who demand support, overwhelming paid-tier service |
| **Behavioral adaptation** | Speed bumps slow traffic, so drivers take residential shortcuts |
| **Resource reallocation** | Automating task A frees time, which gets absorbed by task B, not saved |
| **Selection effect** | Lowering hiring bar changes who applies, which changes culture, which changes retention |

## Remember

- Certainty decreases with each order — second-order effects are probable, third-order are possible
- You don't need to predict everything — just notice that downstream effects *exist*
- Pair with `invert` to check: "What's the worst second-order effect, and can I survive it?"
- The goal isn't paralysis — it's making first-order decisions with second-order awareness
