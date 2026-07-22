# Reasoning Agent Prompt Template

Fill in the 8 inventory file paths, the 8 criteria doc paths (full paths to `references/criteria-*.md`), and the resolved `<workspace>` path, then pass to the reasoning agent (Opus, max effort).

---

You are assessing whether a Claude Code setup has everything in the right configuration layer.

**Read these inventory files:** [list all 8 inventory paths]

**Read these criteria docs** (they define what belongs in each layer and the boundary tests between them): [list all 8 criteria doc paths]

Produce findings in three categories:

**Relocations** — items that exist but are in the wrong layer.
For each: name the item, its current layer, the recommended layer, which boundary test from the criteria docs applies, and what concretely improves.

**Consolidations** — items scattered across layers that serve the same workflow and should be bundled.
For each: list the items, the workflow they serve, and what form the bundle should take (plugin, skill, etc.).

**Net-New** — automations that don't exist but are implied by convergent evidence from multiple existing config items.
For each: what should be created, what config type it should be, and which existing items imply it. Every net-new recommendation must cite evidence from at least two different inventory files. If the evidence doesn't converge from multiple layers, it's speculation — omit it.

**Reasoning rules:**
- Apply the boundary tests from the criteria docs. Training data encodes obsolete boundaries (skills can now fork with pinned models; hooks can carry model-backed handlers). The criteria docs have the current tests.
- For the memory-vs-rule boundary, apply the fuzzy-boundary rule from criteria-memory.md ("Memory vs. Rule"): when fuzzy, resolve to memory.
- Distinguish **broken placement** from **suboptimal placement**. Broken: the current layer causes a concrete problem — wrong loading behavior, missed triggers, capability mismatch. Suboptimal: it works but another layer would serve it better — cleaner scoping, fewer tokens, more appropriate loading semantics. Surface both, but tag each finding as `broken` or `suboptimal` so the user can prioritize.
- Don't recommend consolidating items that touch the same topic but serve different functions.
- **Test for drift tolerance, not just deduplication.** Before flagging hook/rule (or hook/CLAUDE.md) overlap as redundancy, apply the intentional-stacking test from criteria-hooks.md ("Hook vs. Rule"). You may still flag the overlap descriptively, but frame skipping the recommendation as justified when stacking serves drift tolerance.
- **Ignore dead-weight items.** Empty files, no-op scripts, orphaned caches — scanners tag these `[dead-weight]` but cleanup is a separate maintenance concern, not yours. Don't produce findings for them. Focus on placement: is this item in the right layer?
- Rank findings within each category by impact — what would most improve the setup if acted on.

**Systematic boundary sweeps (mandatory):**

Don't cherry-pick — sweep every item through its high-traffic boundary tests. Specifically:

1. **Every CLAUDE.md section with content character "behavioral" or "enforcement"**: test against the rules boundary. Path-specific instructions paying always-on tokens for sometimes-relevant guidance are relocation candidates. Walk each behavioral section, not just the ones that jump out. **Test at the instruction level, not the heading level** — a parent heading ("Critical Operational Rules") cannot receive a batch verdict that cascades to its children. Each sub-rule may have a different boundary answer (one might be path-specific while another is genuinely project-wide). Clear each instruction individually.
2. **Every memory file with content character "behavioral" or "enforcement"**: test against the imperative-voice boundary. A memory that prescribes behavior ("Don't...", "Always...", "When X, do Y") or explicitly extends a named rule file is a relocation candidate. The "resolve fuzzy to memory" preference still applies — but you must examine and state your reasoning, not skip silently.
3. **Every project-scoped item**: test whether it applies to other projects. Every global item: test whether it references project-specific paths or content.
4. **Memory directories that are empty or contain no files**: note this in findings as "Memory: no files present in [project]" — don't silently skip. The user infers the state from what you report.

**Silence is not clearance.** Every item you examine must appear either in findings or in the "Correctly Placed" section — an item that appears in neither is an item you didn't examine, and that's a gap, not an answer. To keep the section readable at scale, group correctly-placed items by config type with a count and the item names; give an individual one-line reasoning only for items that required a boundary test (behavioral CLAUDE.md sections, imperative-voice memory files, project-vs-global scoping calls).

**Output:** Write your full findings to `<workspace>/findings.md` — a numbered list, grouped by category, continuously numbered across categories, with the "Correctly Placed" section at the end. Return only a one-line summary as your reply: finding counts per category and any `broken` items.
