## ai-news

A Claude Code skill that researches Canadian AI industry developments and writes a curated daily digest. Covers funding, jobs, company growth, policy, research, and infrastructure — focused on Ontario and Quebec with a Canada-wide lens.

The skill handles the full pipeline: deduplication against previous issues, multi-source web research with tested fetch strategies, and structured markdown output with geographic tagging and reliability-ranked sources.

### What It Does

When triggered, the skill:

1. Checks if today's digest already exists (no duplicates)
2. Loads the last 5 issues to build an exclusion list (no repeated stories)
3. Runs 4–5 targeted web searches across a tiered source list
4. Fetches and verifies articles from Canadian tech/AI outlets
5. Writes a formatted digest organized by content domain

The output is a markdown file with frontmatter, geographic tags per item, and stories grouped into six sections: Funding/Investment/M&A, Jobs/Talent, Company Growth/Market Moves, Policy/Regulation, Research/Innovation, and Infrastructure/Compute.

### Sample Output

```markdown
## Funding, Investment & M&A

- **[Cohere closes $500M Series D at $5.5B valuation](https://betakit.com/...)** — Toronto-based
  enterprise AI company closes largest Canadian AI round of the year. Round led by PSP Investments
  with participation from Salesforce Ventures. _BetaKit · Ontario_

## Jobs & Talent

- **[Vector Institute expands applied AI residency program](https://vectorinstitute.ai/...)** —
  Program doubles intake to 40 residents for 2026 cohort, adds healthcare and climate streams.
  Partnership with five Ontario hospitals for clinical AI placements. _Vector Institute · Ontario_

## Policy & Regulation

- **[ISED announces $200M AI Compute Access Fund](https://canada.ca/...)** — Federal program
  gives Canadian startups and researchers subsidized access to domestic GPU clusters. Applications
  open Q3 2026. _Canada.ca · Canada_

> [!quote] Minister François-Philippe Champagne — _Canada.ca_
> "Canadian AI companies shouldn't have to go south of the border just to train a model."
```

### Requirements

**Required:**

- Claude Code (CLI)
- Network access (WebSearch + WebFetch)
- Works best with Sonnet or Opus — the skill runs 4–5 web searches and up to 6 fetch calls per run, so lower-tier models may struggle with the multi-phase orchestration

**Optional — the skill works without these but gains capabilities with them:**

| Dependency       | What it adds                                                       | Without it                                                          |
| ---------------- | ------------------------------------------------------------------ | ------------------------------------------------------------------- |
| Obsidian vault   | Frontmatter metadata, vault-relative paths, deduplication via glob | Outputs a plain markdown file; adapt the path and strip frontmatter |
| Agent delegation | Offloads research to a `web-research` subagent for cleaner context | Falls back to inline execution automatically (built-in)             |
| Playwright MCP   | Last-resort fetch for sites that block standard requests           | Skipped automatically; WebFetch + Jina handle most sources          |

### Installation

```bash
# Clone and copy
git clone --depth 1 https://github.com/<user>/<repo>.git
cp -r <repo>/skills/ai-news ~/.claude/skills/

# Create your output directory — wherever you want digests to live
mkdir -p <output-folder>  # e.g., notes/ai-news, digests/, Research/AI/, etc.

# Optional: reduce permission prompts
# Add to .claude/settings.local.json:
# { "permissions": { "allow": ["WebFetch", "WebSearch"] } }
```

The skill triggers on phrases like "Canadian AI news," "AI digest," "Canadian tech industry update," or by invoking `/ai-news` directly.

### Usage

```
/ai-news --output <output-folder>    # run the digest, writing to your chosen folder
/ai-news                             # prompts for output path if not provided
```

The `--output` flag tells the skill where to write digest notes. If omitted, the skill asks you for a path. There is no default — you decide where digests belong in your project.

### How the Source Tiers Work

The skill organizes sources into three tiers to manage fetch budget and signal quality:

**Tier 1 (direct fetch)** — Canadian tech outlets tested for reliable full-text access: BetaKit, The Logic (via Jina), CBC News Business, ISED/Canada.ca. These are worth the WebFetch call because they consistently return clean article text and cover the Canadian AI beat as a primary focus.

**Tier 2 (fetch when needed)** — Ecosystem and institutional sources: Vector Institute, Mila, MaRS, Invest Ontario. Search snippets usually suffice, but when a story is substantive enough to need full context, these sites are fetchable.

**Tier 3 (snippets only)** — Global outlets (TechCrunch, VentureBeat, Reuters) where the Canadian angle is secondary. The search snippet already captures what you need; fetching the full article burns budget for marginal return.

This tier structure is a rate-limit budget strategy. The skill caps total WebFetch calls at 6 per run — the tiers ensure those calls go to the sources most likely to yield Canadian-specific substance.

### Adapting to Other Regions

The skill is built for Canadian AI news, but the architecture is region-agnostic. To adapt it:

1. **Search queries** — Replace "Canada," "Ontario," "Quebec," and city names with your region. If your search tool supports geographic targeting (e.g., Brave Search's `country` parameter), update it to match
2. **Source tiers** — Swap Canadian outlets for your local equivalents and test their fetch behavior (paywall? Jina needed? clean HTML?)
3. **Geographic tags** — Replace the province list with your own sub-regions
4. **Content domains** — Swap government bodies (ISED, IRAP, SR&ED) for your country's equivalents
5. **Output path** — Set `<output-folder>` to your preferred location

The content domain structure (Funding, Jobs, Policy, etc.) and the formatting rules are universal — only the sources and geography need changing.

### Notes for Non-Obsidian Users

The output includes Obsidian frontmatter and `> [!quote]` callout syntax. If you're not using Obsidian, strip the frontmatter block from the output template in SKILL.md. The `[!quote]` callout renders as a plain blockquote with visible `[!quote]` text in standard markdown renderers.
