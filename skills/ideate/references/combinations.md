# Combination Catalog

All sensible mode combinations organized by category. Each entry: the pair, rationale, and a concrete example. Load `orchestration.md` for execution instructions.

## Same-Role Combinations

Run in-context, sequential. No agents. Second step sees first step's output.

### Generative + Generative

1. **`collide+analog`** — Wild collision, then structural validation
   - *Narrative designer inventing a dialogue system. Collide crashes "dialogue" with "jazz improvisation." Analog validates: jazz has real structure (call-and-response, trading fours, resolution) that maps to NPC conversation flow.*

2. **`collide+scaffold`** — Generate through collision, then structure what emerged
   - *Brainstorming a community engagement model. Collide with "ecosystem" produces organic growth metaphors. Scaffold structures it into stages: Seed (founding members), Root (shared rituals), Canopy (public-facing identity), Fruit (member-created content).*

3. **`collide+bound`** — Collide freely, then calibrate which directions to pursue
   - *Marketing a horror game. Collide produces five concepts from different domains. Bound anchors to budget ($5K) and channel (social only), identifying which collisions are feasible vs. which are interesting but impractical.*

4. **`collide+axiom`** — Crash domains, then rebuild from the collision's first principles
   - *Game economy design. Collide with "ecology" produces predator-prey dynamics for player classes. Axiom strips to fundamentals: what must be true about resource flow in this system regardless of the metaphor?*

5. **`axiom+scaffold`** — Rebuild from fundamentals, then structure the result into stages
   - *Rethinking a QA pipeline. Axiom strips to truths: bugs cost more the later they're found, not all bugs are equal. Scaffold structures the rebuild: Gate 1 (core loop playable), Gate 2 (critical paths), Gate 3 (edge cases), Gate 4 (first-time experience).*

6. **`axiom+analog`** — Rebuild from scratch, then check if the result matches a known archetype
   - *Pricing strategy rebuilt from first principles. Axiom produces a transparency-based model. Analog recognizes the structural shape: it matches "open-book pricing" solved by Buffer and Everlane — confirms the rebuild has precedent.*

7. **`axiom+bound`** — Rebuild from fundamentals, then explore the rebuild's boundaries
   - *Redesigning a tutorial from first principles. Axiom produces "teach by doing, never by telling." Bound tests the limits: at what player skill level does pure discovery fail? Where does the 30-50% divergence sweet spot sit for tutorial freedom?*

8. **`analog+scaffold`** — Import a solution from another domain, then give it implementation phases
   - *Building a modding community (cold-start problem). Analog maps from Wikipedia's early strategy. Scaffold phases the rollout: Phase 1 (studio publishes example mods), Phase 2 (featured modder program), Phase 3 (mod marketplace), Phase 4 (community governance).*

9. **`analog+bound`** — Import a structural solution, then test where the mapping holds and breaks
   - *Applying Uber's cold-start strategy to a multiplayer game. Analog maps the structure. Bound calibrates: where does the analogy hold (subsidy gets early adopters) and where does it break (games aren't marketplaces — supply doesn't equal the product)?*

### Adversarial + Adversarial

10. **`assume+invert`** — Surface hidden assumptions, then pre-mortem each one
    - *Planning Early Access launch. Assume surfaces: "players tolerate EA bugs" (standards have risen), "EA generates buzz" (market saturated), "1.0 ships in 12 months" (most take 2-3x). Invert pre-mortems each: scathing reviews, buzz drowned by 20 other EA launches, community churned by month 18.*

11. **`assume+constrain`** — Surface hidden beliefs, then toggle them as constraints to test
    - *Studio assumes "we need a publisher." Assume surfaces the belief. Constrain toggles it: remove the publisher constraint — what changes? Distribution shrinks but creative control expands. Is the publisher a physics constraint or a convention constraint? Test: could direct community building replace publisher reach?*

12. **`assume+subtract`** — Surface hidden beliefs, then remove the ones that don't hold up
    - *Content strategy assumes: weekly cadence matters, SEO drives discovery, long-form outperforms short. Assume surfaces each. Subtract tests: the audience actually discovers through social shares, not search. Remove SEO-driven structure. What's left is the real strategy.*

13. **`steelman+assume`** — Build the opposing case, then dig into your own position's assumptions
    - *You believe single-player only is right. Steelman builds the multiplayer case: 10x lifetime, streaming rewards multiplayer, organic social marketing. Assume turns inward: "Am I assuming single-player can match that retention? Have I tested whether my audience wants social play?"*

14. **`steelman+invert`** — Build the opposing case, then pre-mortem your own position using the steelman's strongest points
    - *Studio head is confident about premium pricing. Steelman builds the F2P case. Invert then pre-mortems premium using steelman's best hits: "The premium game failed because the F2P competitor offered the same content with optional spending, and players chose access over ownership."*

15. **`steelman+subtract`** — Build opposing case, then cut from your position whatever the steelman genuinely defeated
    - *Defending a complex crafting system. Steelman builds the case for "no crafting — just loot." If the steelman genuinely defeats the argument for 3 of your 5 crafting subsystems, subtract removes them. Keep only what survived.*

16. **`subtract+constrain`** — Identify removal candidates, then test which are load-bearing
    - *Design doc with 15 "core features." Subtract flags 6 as inertia-driven. Constrain tests each removal: remove leaderboards → competitive loop still works (remove). Remove crafting → economy collapses, it's the only resource sink (keep). Remove companion app → nobody uses it (remove).*

17. **`invert+subtract`** — Imagine failure, then cut what causes it
    - *Planning a game jam. Invert: "How do we guarantee failure?" — scope too ambitious, silos, no playtesting until final day. Subtract cuts the causes: 10-page design doc (scope source) → 1 page. New engine plan (debate source) → use what we know. Sequential pipeline (silo source) → pair programming.*

18. **`invert+constrain`** — Imagine failure, then test which constraints would prevent each failure mode
    - *Pre-mortem on a live-service launch. Invert identifies: content drought at month 3, server costs exceed revenue at month 6, community toxicity at month 9. Constrain tests: what constraint prevents content drought? Minimum 2-week content cadence. What prevents cost overrun? Player cap until revenue covers infrastructure.*

19. **`constrain+subtract`** — Identify load-bearing vs. decorative constraints, then remove the decorative ones
    - *A game pitch with 12 stated constraints. Constrain classifies: 4 are physics (engine limits, team size), 3 are policy (platform requirements), 5 are convention ("games like this always have X"). Subtract removes the conventions. The pitch tightens from "everything" to "what actually matters."*

### Integrative + Integrative

20. **`lens+simplify`** — Synthesize perspectives, then find the root of their disagreement
    - *Team disagrees on monetization: cosmetics-only, battle pass, seasonal DLC. Lens maps: all agree on post-launch revenue, diverge on acceptable player commitment. Simplify finds root: the team hasn't defined what "fair" means for their players. Three stances, one undefined principle.*

21. **`lens+pattern`** — Synthesize perspectives, then extract what persists across the synthesis
    - *Five playtesters give contradictory feedback. Lens preserves all perspectives without flattening. Pattern extracts: across all five, the consistent signal is confusion about game state — not difficulty, not pacing. The invariant points to a UI problem, not a design problem.*

22. **`lens+timeshift`** — Synthesize perspectives, then view the synthesis from different time horizons
    - *Advisors disagree on studio strategy: focus on one game vs. diversify. Lens synthesizes the perspectives. Timeshift views the synthesis at 1 year (one game is safer), 3 years (diversification spreads risk), 5 years (one breakout game builds more brand value than three mid-tier). The disagreement is actually about time horizon, not strategy.*

23. **`pattern+ripple`** — Extract the recurring signal, then trace its consequences forward
    - *Content creator's top performers all name a problem the audience can't articulate. Pattern extracts: "naming the unnamed frustration." Ripple traces: content strategy shifts from answering known questions to articulating felt problems — which changes SEO strategy entirely (creating demand for new search terms).*

24. **`pattern+simplify`** — Extract the pattern, then find the upstream cause of the pattern
    - *Studio's prototypes keep dying in production. Pattern: same handoff failure in marketing, hiring, and QA. Simplify: the studio has a systemic knowledge-transfer problem — every process that splits "design it" from "build it" into separate teams breaks.*

25. **`timeshift+lens`** — View from multiple time horizons, then synthesize what each reveals
    - *Deciding whether to add mod support (6-month investment). Timeshift views at 1 month (delays launch), 1 year (small community), 3 years (self-sustaining). Lens synthesizes: all horizons agree mods extend life; they diverge on whether upfront cost is justified. Insight: this is a bet on whether the game has platform potential.*

26. **`timeshift+simplify`** — View from multiple horizons, then find the root that all horizons point to
    - *Career decision: safe contract vs. passion project. Timeshift views from multiple horizons. Simplify finds: every horizon where the passion project wins depends on the same assumption — that the project is portfolio-defining. The root question isn't risk tolerance, it's project quality.*

27. **`timeshift+pattern`** — View from multiple horizons, then extract what matters across all of them
    - *Evaluating a studio's project pipeline. Timeshift views each project at 1-year and 3-year marks. Pattern extracts: the projects that matter at BOTH horizons all share one trait — they build an audience asset (community, IP, tool), not just a product. Projects without audience-building decay to zero value.*

28. **`simplify+ripple`** — Find root cause, then trace the consequences of fixing it
    - *Studio's three fires (unclear briefs, changing requirements, "fixed" bugs reappearing) trace to one root: no living design doc. Simplify finds the root. Ripple traces forward: if we fix it, first-order — communication improves. Second-order — the doc becomes a bottleneck (who maintains it?). Third-order — the doc maintainer role becomes the most important hire.*

29. **`simplify+pattern`** — Find root cause, then check if the root is a recurring meta-pattern
    - *Simplify identifies why this project's onboarding fails: information is scattered across 6 documents. Pattern checks: same root in customer support (scattered knowledge), in team onboarding (scattered docs), in QA (scattered test plans). Meta-pattern: the org has a single-source-of-truth problem everywhere.*

30. **`ripple+lens`** — Trace multiple consequence chains, then synthesize what they reveal together
    - *Considering three pricing changes. Ripple traces each chain independently: free tier attracts non-payers, price increase loses casual buyers, bundling cannibalizes individual sales. Lens synthesizes: all three chains converge on the same tension — the studio can optimize for reach OR revenue-per-user, but each pricing move trades one for the other.*

31. **`ripple+simplify`** — Trace consequence chains, then find the shared root they converge on
    - *Three proposed features each have concerning second-order effects. Ripple traces each. Simplify finds: all three consequence chains lead to the same bottleneck — the support team. Every feature that increases user options increases support load. The root constraint isn't engineering capacity, it's support capacity.*

## Cross-Role Combinations

Ask the user: in-context (faster, shared reasoning) or independent agents (stronger independence)? Load `orchestration.md` for execution details.

### Generative → Adversarial

32. **`axiom+invert`** — Rebuild from first principles, then pre-mortem the rebuild
    - *Indie studio rebuilds go-to-market: find 100 niche forum users, give them early access, let them amplify. Invert (fresh eyes): "This failed. What killed it?" The 100 people had no reach. The forums had 500 members total. Organic spread works for social products, not games.*

33. **`axiom+assume`** — Rebuild from fundamentals, then excavate remaining hidden assumptions
    - *Rebuilt pricing from first principles: price-per-hour-of-content. Assume finds the hidden belief: "players evaluate games by hours of content." Many don't — they evaluate by peak moments, by emotional impact, by replayability. The rebuild inherited an assumption from conventional pricing without noticing.*

34. **`axiom+steelman`** — Rebuild from scratch, then steelman the conventional approach you discarded
    - *Rebuilt the hiring process from first principles: skills tests only, no interviews. Steelman defends the conventional interview: it tests collaboration style, communication, culture fit — things a skills test can't measure. The rebuild may have thrown out signal with the noise.*

35. **`axiom+subtract`** — Rebuild from scratch, then test what can be removed from the rebuild
    - *Rebuilt a game's progression system from fundamentals. Subtract asks: of the rebuilt system, what's actually load-bearing? The XP curve is essential but the prestige ranks are decorative — remove them. Even first-principles rebuilds can overshoot.*

36. **`axiom+constrain`** — Rebuild from scratch, then test against real-world constraints
    - *First-principles redesign of a game's economy. Constrain tests: with a 3-person team, which parts of the redesign are buildable? With existing tech, which require new systems? The rebuild is ideal but the constraints reveal what's shippable.*

37. **`collide+steelman`** — Wild idea, then strongest case against it
    - *Marketing collides horror game with "therapy": exposure therapy for the digital age. Steelman against: trivializing therapy alienates the mental health community, the framing attracts help-seekers not horror fans, and it creates liability if anyone claims the game worsened anxiety. Creative but reputation-ending.*

38. **`collide+invert`** — Generate through collision, then pre-mortem the best collision
    - *Collide "city-builder" with "cooking." The collision produces: city as recipe, ingredients are resources, technique is placement, timing is development sequence. Invert: "This game concept failed. What killed it?" — the cooking metaphor made players expect a linear sequence, but city-builders need open-ended play. The metaphor constrained the design.*

39. **`collide+assume`** — Wild collision, then surface what the collision assumes
    - *Collide "multiplayer game" with "improv comedy." The collision assumes players want to collaborate, that failure is funny not frustrating, that audience enjoyment matters as much as player enjoyment. Assume finds: the collision only works if the game treats failure as entertainment, not punishment.*

40. **`collide+subtract`** — Generate through collision, then strip the collision to its essential transfer
    - *Collide "dialogue system" with "poker." The collision produces: bluffing, reading tells, raising stakes, folding. Subtract tests each: bluffing transfers (NPCs can deceive), reading tells transfers (body language cues), raising stakes transfers (escalation), folding doesn't transfer (players don't want to abandon conversations). Strip to three elements.*

41. **`scaffold+invert`** — Build a progression structure, then pre-mortem each stage
    - *Scaffold builds a community growth pipeline: Seed → Root → Canopy → Fruit. Invert pre-mortems each transition: Seed→Root fails when founding members burn out. Root→Canopy fails when internal culture clashes with public perception. Each transition becomes a risk to mitigate.*

42. **`scaffold+assume`** — Create a framework, then surface the assumptions each stage makes
    - *Scaffold builds a game dev pipeline: Prototype → Vertical Slice → Alpha → Beta → Launch. Assume surfaces: every stage assumes the previous stage's output is reliable. What if the prototype validated the wrong thing? The framework inherits error forward — each stage needs its own validation gate.*

43. **`scaffold+subtract`** — Build structure, then remove unnecessary stages
    - *Scaffold creates a 7-stage approval process. Subtract asks: "Would I add this stage if starting fresh?" Four stages exist because of past incidents, not current risk. Two are redundant with each other. Cut to 3 stages — same risk coverage, half the friction.*

44. **`analog+assume`** — Import a solution, then excavate assumptions in the mapping
    - *Map from Uber's cold-start: subsidize creators to attract players. Assume: "This assumes creators drive player acquisition the way drivers drive rider acquisition. But Uber's supply IS the product. Creators are amplifiers, not the product. The analogy works for marketplaces, not entertainment."*

45. **`analog+invert`** — Import a structural solution, then pre-mortem the imported version
    - *Import airline loyalty program structure for a game. Invert: "The loyalty program failed. What killed it?" — play-time rewards attracted grinders not spenders. Exclusive content was expensive to produce for a small elite tier. The airline model assumes scarcity drives desire, but games aren't uncomfortable — there's no pain to escape.*

46. **`analog+steelman`** — Import a solution, then steelman the case against the mapping
    - *Mapped a game's progression from RPG leveling systems. Steelman against: "RPG leveling assumes power growth equals engagement. Your game is a puzzle game — players don't want to become more powerful, they want more interesting challenges. Leveling solves the wrong problem."*

47. **`bound+invert`** — Explore within calibrated scope, then pre-mortem the exploration boundaries
    - *Bound sets the exploration space for a new game genre: "somewhere between roguelike and narrative RPG." Invert: "This scope failed. Why?" — too broad, the team explored for 6 months without converging. Or too narrow — excluded the best ideas because they didn't fit the pre-set box.*

### Generative → Integrative

48. **`collide+lens`** — Multiple collisions in parallel, then synthesize what they reveal
    - *Three collision agents reimagine a city-builder: collision with ecology, cooking, and music. Lens synthesizes: all converge on "living system with rhythm," diverge on what the player does. Ecology says "maintain equilibrium," cooking says "follow a recipe," music says "harmonize competing instruments." Recipe is weakest for open-ended play.*

49. **`collide+ripple`** — Generate through collision, then trace the collision's consequences forward
    - *Collide "job board" with "matchmaking." The collision produces: compatibility scoring, mutual opt-in, rejection as information. Ripple traces: if implemented, first-order — better matches. Second-order — employers game the compatibility score. Third-order — an arms race between authentic profiles and optimized profiles, exactly like dating apps.*

50. **`collide+pattern`** — Multiple collisions, then extract what persists across them
    - *Collide "tutorial" with five different domains: escape room, first date, apprenticeship, theme park, therapy session. Pattern: the collisions that work best all share one trait — they give the player agency over the pace. The invariant is player-controlled pacing, not any specific metaphor.*

51. **`collide+simplify`** — Multiple collisions, then find the upstream unification across them
    - *Collide "retention" with three domains: habit loops (psychology), symbiosis (biology), gravitational pull (physics). Simplify: all three collisions point to the same upstream mechanism — the thing you return to must change each time you engage with it. Stale content = decaying orbit = parasitism = broken habit loop.*

52. **`axiom+lens`** — Rebuild from scratch, then synthesize the rebuild with existing perspectives
    - *Axiom rebuilds the content pipeline from first principles. Lens synthesizes the rebuild with the existing team's perspective: the rebuild is technically superior but ignores institutional knowledge — the current pipeline's "inefficiencies" encode tacit team preferences that the rebuild discarded.*

53. **`axiom+ripple`** — Rebuild from fundamentals, then trace the consequences of adopting the rebuild
    - *Axiom redesigns team structure from first principles. Ripple traces: first-order — roles are clearer. Second-order — specialists lose their informal influence networks. Third-order — decisions that used to happen through hallway conversations now require formal proposals, slowing response time.*

54. **`axiom+pattern`** — Rebuild, then check what you inadvertently re-derived
    - *Axiom rebuilds a game's combat system from scratch. Pattern compares with the old system: 70% of the rebuild matches the existing design. The 30% that changed reveals which parts of the old system were convention (discarded) vs. principled (re-derived). The 70% overlap validates the existing design.*

55. **`analog+lens`** — Import a solution, then synthesize the import with local domain knowledge
    - *Analog imports community governance from open-source projects (meritocratic maintainers, pull-request culture). Lens synthesizes with game community norms: open-source governance assumes contributors are skilled and self-selected. Game communities are broader — governance needs moderation (managing bad actors), not just meritocracy (elevating good ones).*

56. **`analog+ripple`** — Import a solution, then trace its consequences in the target domain
    - *Import Spotify's discovery algorithm for game recommendations. Ripple: first-order — players discover more games. Second-order — small games get buried by algorithmic preference for engagement metrics. Third-order — developers optimize for algorithmic visibility instead of quality, exactly like SEO content farming.*

57. **`scaffold+lens`** — Build a progression structure, then synthesize with stakeholder views
    - *Scaffold builds a 4-stage product roadmap. Lens synthesizes with engineering, design, and business perspectives: engineering says Stage 2 is technically impossible without Stage 3's infrastructure. Business says Stage 4 needs to come first for revenue. The scaffold's sequence was logical but ignored dependency realities.*

58. **`scaffold+ripple`** — Create a framework, then trace what each stage enables and prevents
    - *Scaffold creates a community growth pipeline. Ripple traces each transition: Seed→Root enables organic culture but prevents rapid scaling. Root→Canopy enables visibility but creates culture clash risk. Each stage's benefit is the next stage's constraint.*

59. **`scaffold+simplify`** — Build structure, then find the single principle that governs the progression
    - *Scaffold creates a 5-stage learning path for game design. Simplify finds: the progression isn't actually 5 stages — it's one principle (make → test → learn) repeated at increasing scale. The "stages" are just different scopes of the same loop.*

### Adversarial → Integrative

60. **`assume+lens`** — Surface assumptions from multiple perspectives, then synthesize
    - *Three agents each run assume from a different stakeholder: player assumptions ("progression = power"), designer assumptions ("balance requires gating"), business assumptions ("retention requires daily logins"). Lens synthesizes: all three assume "engagement" matters but define it differently — freedom, control, frequency.*

61. **`assume+pattern`** — Surface assumptions, then extract the pattern of what was hidden
    - *Assume across five areas of the project. Pattern extracts: every hidden assumption traces to one source — the studio's last successful game. The team is unconsciously designing the sequel, not a new game. The meta-pattern is "anchoring to past success."*

62. **`assume+ripple`** — Surface hidden beliefs, then trace what happens if each is wrong
    - *Assume surfaces: "our audience is male, 18-35." Ripple traces: if wrong, marketing is reaching the wrong demographic, game features are optimized for the wrong preferences, community management is using the wrong tone. One wrong assumption cascades through every department.*

63. **`assume+simplify`** — Surface assumptions, then find the one root assumption driving all others
    - *Assume surfaces eight hidden beliefs about a project. Simplify finds: six of the eight derive from one root assumption — "we're competing with AAA studios." Remove that root and the others evaporate. The studio isn't competing with AAA; it's serving a niche AAA ignores.*

64. **`invert+lens`** — Pre-mortem from multiple perspectives, then synthesize failure modes
    - *Three agents pre-mortem a game launch from different angles: player reception, financial viability, team sustainability. Lens synthesizes: all three identify the same root risk — scope creep. But each traces it to a different consequence: players get a shallow game, finances stretch past break-even, team burns out.*

65. **`invert+ripple`** — Imagine failure, then trace the failure chains forward
    - *Invert identifies: "The live-service game failed because the content pipeline couldn't keep up." Ripple traces the chain: content drought → community frustration → negative reviews → new player acquisition drops → revenue drops → further content budget cuts → death spiral.*

66. **`invert+simplify`** — Pre-mortem, then find the root vulnerability across failure modes
    - *Invert identifies five failure modes for a product launch. Simplify finds: three of the five share one root — the team hasn't validated demand. The launch assumes interest based on internal excitement, not market evidence. Fix the validation gap and three failure modes disappear.*

67. **`steelman+simplify`** — Build opposing case, then find the root of the real disagreement
    - *Self-publish vs. publisher. Steelman builds the publisher case. Simplify finds the root: both sides agree on the goal. The real disagreement is audience type — discoverable (publisher helps) vs. already known (self-publish). The question is audience shape, not distribution strategy.*

68. **`steelman+lens`** — Build opposing case, then synthesize both positions
    - *Steelman builds the case against the team's chosen art style. Lens synthesizes: the team's style is more distinctive but harder to market; the steelmanned alternative is more accessible but less memorable. The synthesis reveals the real decision: optimize for first impression (marketing) or for long-term identity (brand)?*

69. **`steelman+ripple`** — Build opposing case, then trace consequences if the opposition is right
    - *Steelman builds the case for F2P over premium. Ripple traces: if the steelman is right, second-order — the studio needs to build live-ops capability it doesn't have. Third-order — hiring for live-ops changes team culture from "craft" to "service." Is the studio willing to become a different kind of company?*

70. **`subtract+lens`** — Identify removal candidates, then synthesize stakeholder views on each removal
    - *Subtract flags 4 features for removal. Lens gathers perspectives: engineering says feature A is cheap to maintain (keep), design says feature B is beloved by a small passionate group (keep?), business says feature C has zero engagement metrics (remove). Each removal decision has a different stakeholder profile.*

71. **`subtract+pattern`** — Remove things, then extract what the removals reveal
    - *Subtract removes six features from a game. Pattern: the removed features all share one trait — they were added to match competitor feature lists, not to serve the game's core loop. The meta-pattern: the game has a "competitive mimicry" problem in its design history.*

72. **`constrain+lens`** — Toggle constraints, then synthesize what each toggle reveals
    - *Constrain removes budget, time, and team-size constraints one at a time. Lens synthesizes: removing budget doesn't change the design (it's already cheap to build). Removing time changes everything (the team would prototype three ideas instead of committing to one). The time constraint is the real bottleneck, not budget.*

73. **`constrain+simplify`** — Toggle constraints, then find the single constraint that matters most
    - *Constrain tests six constraints. Simplify finds: four of the six are downstream of one — the platform constraint (must ship on console). Remove that constraint and budget, timeline, team size, and certification requirements all relax. The root constraint is the platform decision.*

### Integrative → Adversarial

74. **`lens+steelman`** — Synthesize perspectives, then champion the one the synthesis underweighted
    - *Team debates tone: dark-serious, dark-humor, lighthearted. Lens synthesizes: "dark world, humanizing humor." But "lighthearted" got compressed. Steelman: "Dark-serious competitors are saturated. Hades proved dark-themes-with-light-tone is underserved. Lighthearted isn't naïve; it's the commercial differentiator."*

75. **`lens+invert`** — Synthesize perspectives, then pre-mortem the synthesis
    - *Lens synthesizes team views into a hybrid monetization model. Invert: "This hybrid failed. Why?" — it tried to please everyone and satisfied no one. Cosmetics-only players felt the battle pass was predatory. Battle pass players felt the cosmetics-only content was locked behind a paywall. The synthesis was a compromise, not a strategy.*

76. **`lens+assume`** — Synthesize, then surface assumptions the synthesis inherited from the dominant perspective
    - *Lens synthesizes four team members' views on launch strategy. But the synthesis skews toward the most senior voice. Assume: "What assumptions did the synthesis inherit from the director's perspective? That AAA marketing tactics apply to indie. That Day 1 sales determine success. That press coverage matters more than community building."*

77. **`pattern+steelman`** — Extract the invariant, then steelman the opposing pattern
    - *Pattern extracts: the studio's successful games all launched with small, dedicated communities. Steelman against: "The successful games were all in genres with built-in core audiences. The next game is in a genre without one. The pattern isn't 'small launches work' — it's 'small launches work when the audience self-selects.' You don't have that luxury this time."*

78. **`pattern+invert`** — Extract the signal, then pre-mortem relying on it
    - *Pattern extracts: every project that shipped on time had a single decision-maker. Invert: "We relied on this pattern and failed. Why?" — the decision-maker was wrong about a key creative call, and nobody could course-correct because the pattern said trust the one voice. The pattern works until the decision-maker's blind spots become the project's blind spots.*

79. **`simplify+steelman`** — Find root cause, then steelman that it's the wrong root
    - *Simplify identifies: the studio's retention problem is caused by weak onboarding. Steelman: "The strongest case that onboarding ISN'T the root: your retained players also had rough onboarding but stayed anyway. What they have in common isn't a good first hour — it's a social connection (guild, friend, streamer). The root isn't onboarding, it's social hooks."*

80. **`simplify+invert`** — Find root cause, then pre-mortem fixing it
    - *Simplify finds: the root cause of three project failures is no living design doc. Invert: "We implemented the living design doc and it failed. Why?" — nobody maintained it after the first month. Or: the doc became a political document (people wrote what stakeholders wanted to read, not what was true). The fix has its own failure modes.*

81. **`timeshift+steelman`** — View from multiple horizons, then steelman the horizon you dismissed
    - *Timeshift suggests the 5-year view favors the passion project. Steelman the 1-week view: "Bills are real. Reputation for reliability is built by taking the contract. The 'safe' choice isn't just about money — it's about professional relationships that compound. The freelancer who always delivers gets offered better projects."*

82. **`timeshift+invert`** — View from multiple time horizons, then pre-mortem across them
    - *Timeshift views a feature investment at 3 months, 1 year, 3 years. Invert pre-mortems each: at 3 months the feature isn't finished (scope creep). At 1 year the market has moved on (the feature solves yesterday's problem). At 3 years the tech stack has changed and the feature needs a full rewrite.*

83. **`ripple+steelman`** — Trace consequence chains, then steelman that the consequences are acceptable
    - *Ripple traces: adding a free tier leads to community culture shift, support burden, paying player dissatisfaction. Steelman: "These consequences are the cost of growth, and they're manageable. Every successful F2P game went through this transition. The culture shift is maturation, not degradation. Support burden is a hiring problem, not a model problem."*

### Integrative → Generative

84. **`simplify+axiom`** — Find root cause, then rebuild from it as a first principle
    - *Studio keeps failing at live-service. Simplify finds: the team thinks in game dev cycles, not service cycles. Axiom (new agent, given only this root): rebuilds from "we are building a service." Service-oriented roles, continuous content pipeline, retention metrics over review scores. Bolder because the agent didn't go through the diagnosis.*

85. **`simplify+collide`** — Find root cause, then collide it with unexpected domains for novel solutions
    - *Simplify finds: the root of community churn is that members consume but don't contribute. Collide: "What if contribution was farming?" — you plant (share an idea), tend (respond to others), harvest (get recognition). The agricultural metaphor produces a contribution system with natural rhythms and seasons.*

86. **`pattern+axiom`** — Extract the pattern, then rebuild a solution from the pattern as a first principle
    - *Pattern extracts: every failed feature launch skipped user validation. Axiom takes "no feature launches without validation" as a fundamental truth and rebuilds the development process around it — validation gates at concept, prototype, and pre-launch, not just post-launch analytics.*

87. **`pattern+collide`** — Extract the invariant, then collide it with a new domain
    - *Pattern: the studio's best games all have "one more turn" syndrome — the core loop is so tight players can't stop. Collide "one more turn" with "addiction recovery": what makes the loop compelling without being exploitative? The collision produces ethical retention design — compelling but with natural stopping points.*

88. **`lens+axiom`** — Synthesize perspectives, then rebuild from the synthesis
    - *Lens synthesizes: the team agrees on "make it accessible" but means different things. Axiom strips "accessibility" to fundamentals: the game must be learnable without instruction, playable without dexterity, and enjoyable without prior genre knowledge. Rebuild the onboarding from these three axioms.*

89. **`lens+collide`** — Synthesize perspectives, then collide the synthesis with a new domain
    - *Lens finds the team's core tension: efficiency vs. craft. Collide with "wine-making": efficiency is mass production (consistent, scalable), craft is terroir (unique to place and maker). The collision produces a framework: automate the repeatable parts (efficiency) to create space for the irreplaceable parts (craft).*

### Adversarial → Generative

90. **`assume+axiom`** — Surface assumptions, then rebuild from scratch without them
    - *Assume surfaces: "games need a tutorial," "players expect save systems," "games should have menus." Axiom takes none of these as given and rebuilds: a game that teaches through environmental clues, auto-saves via world state, and starts instantly with no menu. The assumptions were conventions, not requirements.*

91. **`assume+collide`** — Surface hidden beliefs, then collide the deconstructed space with a new domain
    - *Assume surfaces the game industry's assumption that "games are products you buy." Collide with "public infrastructure": what if games were maintained like parks — funded communally, freely accessible, improved by public investment? The collision produces a games-as-public-goods model.*

92. **`invert+axiom`** — Pre-mortem, then rebuild to prevent the identified failures
    - *Invert identifies: the game will fail because the first 5 minutes are boring. Axiom rebuilds the opening from this constraint as a first principle: "the first action the player takes must produce the most surprising result in the game." Build the entire intro around maximizing first-action impact.*

93. **`subtract+collide`** — Clear the slate, then generate via collision into the cleared space
    - *Subtract removes everything non-essential from a bloated game design. What remains: one character, one mechanic, one environment. Collide this minimal core with "origami": the single mechanic folds the environment into new configurations, each fold revealing new possibilities. Minimalism becomes the creative constraint.*

94. **`steelman+axiom`** — Build the strongest opposing case, then rebuild your position incorporating its strongest points
    - *Your position: the game should be co-op only. Steelman builds the solo case. Axiom rebuilds co-op from scratch, but incorporating the steelman's best insight — that some players want to experience the story alone. Rebuild: co-op is primary but the game scales to solo without losing its identity.*

## Three-Mode Pipelines

Always spawn agents. Load `orchestration.md` for the full execution sequence.

### Generative → Adversarial → Integrative

95. **`collide+steelman+lens`** — Generate, attack, synthesize
    - *Reinventing the tutorial. Three collide agents: "escape room," "first date," "apprenticeship." Steelman attacks each: escape room frustrates, first date front-loads, apprenticeship patronizes. Lens synthesizes: all three steelmans converge on one weakness — each assumes a single onramp. Insight: the tutorial should be three paths, and the game detects which to serve.*

96. **`axiom+invert+simplify`** — Rebuild, pre-mortem, find root vulnerability
    - *Rethinking indie pricing. Axiom: price per expected hour + trust refund. Invert: players gamed refunds, $/hour underpriced short games, support overhead exceeded benefit. Simplify: all failures stem from giving pricing control to the player. Fix: keep transparency, remove player-controlled mechanisms.*

97. **`analog+assume+ripple`** — Import, excavate, trace consequences
    - *Loyalty program mapped from airline miles. Analog: play hours = miles. Assume: mapping assumes playtime = loyalty, but airlines reward spending, not sitting. Ripple: rewarding grinders over spenders inverts the revenue model — second-order, you fund rewards for non-paying "VIPs."*

98. **`axiom+steelman+lens`** — Rebuild, steelman conventional, synthesize
    - *Axiom rebuilds hiring: skills tests only, no interviews. Steelman defends interviews: they test collaboration, communication, culture fit. Lens synthesizes: the rebuild finds better individual contributors, interviews find better team members. The real question is which gap hurts more.*

99. **`collide+invert+simplify`** — Collision, pre-mortem, root cause
    - *Collide "game economy" with "ecology." Invert: "The ecology-based economy failed — predator-prey balance was impossible with human players who min-max." Simplify finds the root: ecological balance requires distributed decision-making, but game economies have concentrated actors (guilds, whales) who break emergent balance.*

100. **`analog+invert+lens`** — Import, stress-test, synthesize with local knowledge
     - *Analog imports open-source governance for a game mod community. Invert: "Governance failed — meritocracy became oligarchy as early contributors gatekept newcomers." Lens synthesizes the import with game community norms: open-source governance assumes intrinsic motivation, but mod communities mix intrinsic (passion) with extrinsic (fame, monetization). Governance needs to account for both.*

101. **`scaffold+assume+pattern`** — Structure, excavate, extract signal
     - *Scaffold builds a 5-stage dev pipeline. Assume surfaces: each gate assumes the previous gate's output is reliable. Pattern checks across past projects: stages 2 and 4 consistently produce unreliable output. The invariant: the pipeline's odd-numbered stages validate, even-numbered stages produce. Re-sequence so every production stage is followed by a validation stage.*

102. **`collide+assume+lens`** — Collision, excavation, synthesis
     - *Collide "game marketing" with three domains: political campaigning, street performance, and disease transmission. Assume excavates what each collision takes for granted. Lens synthesizes: the campaign metaphor assumes you need to convince people; the street performance assumes you need to captivate them; the transmission metaphor assumes it spreads on its own. The synthesis: marketing needs all three — convince early adopters, captivate the mainstream, then design for organic spread.*

103. **`axiom+assume+ripple`** — Rebuild, excavate remaining assumptions, trace consequences
     - *Axiom rebuilds studio culture from fundamentals. Assume finds assumptions the rebuild inherited: "transparency is always good" (sometimes information overwhelms), "flat hierarchy = empowerment" (sometimes it = confusion). Ripple traces: if both assumptions are wrong, the rebuilt culture produces anxious, directionless teams instead of empowered ones.*

### Other Pipeline Shapes

104. **`assume+axiom+lens`** — Excavate, rebuild, synthesize (Adversarial → Generative → Integrative)
     - *Assume surfaces: the game assumes players read. Axiom rebuilds UI from "players don't read" as a fundamental truth: every piece of information is communicated visually, spatially, or through sound. Lens synthesizes the rebuild with the existing design: some text-heavy systems (inventory, quest logs) can't be fully replaced — find the hybrid.*

105. **`invert+collide+lens`** — Pre-mortem, generate alternatives, synthesize (Adversarial → Generative → Integrative)
     - *Invert identifies: the game's launch will fail because the trailer doesn't communicate the core loop. Collide generates three alternative trailer concepts by collision with film genres (documentary, thriller, comedy). Lens synthesizes: the documentary collision communicates gameplay most clearly but isn't exciting. The thriller collision is exciting but misleading. Best hybrid: documentary structure with thriller pacing.*

106. **`subtract+axiom+ripple`** — Clear, rebuild, trace forward (Adversarial → Generative → Integrative)
     - *Subtract strips a bloated game to its minimum viable core. Axiom rebuilds from that core as a first principle. Ripple traces: rebuilding from the stripped core means some players lose features they relied on — second-order, you need a migration plan, not just a redesign.*

107. **`lens+steelman+axiom`** — Synthesize, challenge, rebuild (Integrative → Adversarial → Generative)
     - *Lens synthesizes five team members' visions for the next game. Steelman challenges the consensus: "The strongest case against this direction is that it optimizes for the team's strengths, not the market's gaps." Axiom rebuilds from "serve the market gap" as a first principle — produces a different game concept than the team's comfort zone.*

108. **`pattern+invert+collide`** — Extract signal, stress-test, generate alternatives (Integrative → Adversarial → Generative)
     - *Pattern extracts: the studio's successes all had strong community involvement during development. Invert: "We relied on community involvement and failed — the community's feedback optimized for vocal minority preferences." Collide generates alternative community models by collision with jury selection (random sampling), scientific peer review (structured critique), and beta testing (task-based evaluation).*

109. **`simplify+steelman+axiom`** — Find root, challenge root, rebuild (Integrative → Adversarial → Generative)
     - *Simplify identifies: the studio's growth problem is caused by founder dependency. Steelman: "The strongest case that founder dependency ISN'T the root — the founder's taste is the product's differentiator. Remove the dependency and you remove what makes the studio special." Axiom rebuilds with both truths: "the founder's taste must be encoded in process, not dependent on presence."*

110. **`lens+subtract+axiom`** — Synthesize, clear, rebuild (Integrative → Adversarial → Generative)
     - *Lens synthesizes customer feedback, team feedback, and market data on the product. Subtract cuts: of everything surfaced, which isn't worth responding to? Remove noise, keep signal. Axiom rebuilds the product roadmap from only the surviving signals as first principles.*

## Excluded

**`state` does not appear in combinations.** It is a cognitive mode router — it diagnoses which state you're in and which framework to apply. If a user requests a combination involving `state`, explain: "`state` diagnoses which mode to use. Run `/ideate state` first to identify the right framework, then invoke that framework (with or without a combination)."

## Unlisted Combinations

If a user requests a combination not in this catalog:

> "This combination isn't cataloged, but I can run it. The modes are {role1} and {role2}, so based on the decision tree: {same-role → in-context | cross-role → ask preference | three-mode → agents}. Proceed?"

Not every possible permutation is listed. The catalog covers combinations with clear rationale and productive tension. Unlisted pairs may still work — the execution logic applies regardless of whether the pair is cataloged.
