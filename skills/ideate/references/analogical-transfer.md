# Analogical Transfer ("Structural Mapping")

**Core operation:** Find a structurally similar solved problem in a different domain and map its solution onto your unsolved problem. Not random collision — deliberate structural matching.

## Why It Works

Many problems share deep structural properties across domains: network effects, chicken-and-egg dynamics, tragedy of the commons, principal-agent problems. If you can identify the *shape* of your problem, you can search for domains that solved that shape — and import their solution logic.

## Process

1. **Abstract your problem** — Strip away domain-specific details. What's the structural shape? (e.g., "I need two groups to adopt simultaneously", "I need to coordinate without central authority")
2. **Name the archetype** — Does this match a known structural pattern? (See catalog below)
3. **Search for solved instances** — What domains have faced and solved this exact shape?
4. **Map the solution** — Translate the source solution into your domain's terms
5. **Check the disanalogies** — Where does the mapping break? Those are your risks

## Structural Archetype Catalog

| Archetype | Shape | Domains That Solved It |
|-----------|-------|----------------------|
| **Chicken-and-egg** | Need supply and demand simultaneously | Marketplaces, platforms, dating apps |
| **Tragedy of the commons** | Individual incentives deplete shared resource | Fisheries, open source, shared infrastructure |
| **Principal-agent** | Someone acts on your behalf but has different incentives | Management, real estate, politics |
| **Cold start** | System is useless until critical mass | Social networks, languages, phone systems |
| **Coordination without authority** | Need alignment without top-down control | Open source, jazz ensembles, flocking birds |
| **Signal vs. noise** | Valuable information buried in irrelevant data | Search engines, medical diagnosis, hiring |
| **Exploration vs. exploitation** | Invest in learning or capitalize on what you know? | Foraging theory, A/B testing, career moves |

## Applications

| Your Problem | Structural Match | Source Domain |
|-------------|-----------------|---------------|
| "Users won't join without content" | Cold start | How did early Wikipedia get articles? |
| "Team won't self-organize" | Coordination without authority | How do open-source projects govern? |
| "Freelancers cut corners" | Principal-agent | How do insurance companies align incentives? |
| "Everyone's dumping work on shared resources" | Tragedy of the commons | How did fisheries create quotas? |

## Red Flags You Need This

- "This feels like a known problem" — your intuition is recognizing structural similarity
- "Surely someone's solved this in a different field"
- The problem has clear structural properties (network effects, incentive misalignment, bootstrapping)
- You're the first in your domain to face this, but the *shape* is ancient

## Mapping Prompts

- "What's the shape of this problem if I remove all domain-specific details?"
- "What other system has this exact dynamic?"
- "How did [biology/economics/game theory/urban planning] solve this shape?"
- "What's the closest solved analog — and where does the analogy break?"

## Distinction from `collide`

`collide` (Forced Recombination) crashes **random** domains together to spark creativity. `analog` is **deliberate** — you identify the structural shape first, then search for matching shapes. `collide` is generative chaos; `analog` is structural detective work.

## Remember

- The power is in abstracting the shape, not the surface details
- Disanalogies are as valuable as analogies — they reveal where the mapping needs adaptation
- The best source domains are ones with deep theory: biology, economics, game theory, information theory
- Pair with `bound` to test whether the transferred solution holds at your scale and edge cases
