---
name: ai-news
description: Use when generating Canadian AI industry news digests, researching AI news for Ontario/Quebec/Canada, or running /ai-news. Covers funding, jobs, growth, regulation, market moves. Triggers on Canadian AI news, Canadian tech industry update, AI digest request.
argument-hint: <output-folder>
---

## Canadian AI Industry News (Mon–Fri)

Research AI industry developments in Canada since the last issue and write a curated digest note. Output is a markdown file with frontmatter, compatible with Obsidian vaults (see README for non-Obsidian use). Focused on **Ontario and Quebec** with a broader **Canada-wide** lens. Covers business, labor, policy, and technology — not product reviews or AI hype commentary.

**Arguments:** `/ai-news [--output <path>]`

- `--output <path>` — Directory where digest notes are written (required on first run; ask the user if not provided)

**Schedule:** This skill runs weekdays — **Monday through Friday**.

---

### Phase 0: Resolve Output Path

Resolve the output directory from the `--output` argument. If not provided, ask the user: *"Where should AI news digests be written? Provide a directory path."* Do not assume a default — the user decides where these files belong.

Ensure the output directory exists (create it if needed).

---

### Phase 1: Day-of-Week Check

Before anything else, check if today is a weekday (Monday–Friday).

- If **yes**: proceed to Phase 1.5
- If **no**: report that this digest runs on weekdays only, and stop

---

### Phase 1.5: Deduplication Check

Check if today's note already exists:

```
Glob: <output-folder>/{YYYY-MM-DD}*
```

If a note exists for today, **stop immediately** and report that the digest already exists. Do not overwrite or append.

---

### Phase 2: Load Previous Reports

Find the 5 most recent previous reports to avoid repeating coverage:

```
Glob: <output-folder>/*.md
```

Take the 5 most recent filenames (by date prefix, excluding today's). For each, use **Grep** to extract only:

- The `source:` frontmatter line (contains all article URLs)
- Lines matching `^\- \*\*\[` (bolded headline entries)

Do **not** read the full files. Aggregate extracted URLs and headlines into a single **exclusion list**. During Phase 3, skip any story whose URL or headline substantially matches an item on this list.

If fewer than 5 previous reports exist, use all available. If none exist, proceed without an exclusion list.

---

### Phase 3: Research

**Delegate this phase to a `web-researcher` agent if one is available.** This is an optional custom agent type — most installations won't have one, and the skill falls back to inline execution automatically. If the Agent tool call fails for any reason, **do not retry** — fall back immediately to executing the research inline using the same instructions.

#### Agent Brief

When delegating, pass the agent a brief containing:

1) Today's date
2) The exclusion list from Phase 2 (URLs and headlines to skip)
3) The search queries, source tiers, and WebFetch rules below
4) **Explicit instruction to categorize each finding** into one of the 6 content domains (Funding/Investment/M&A, Jobs/Talent, Company Growth/Market Moves, Policy/Regulation, Research/Innovation, Infrastructure/Compute) — the agent must return findings grouped by section, not as a flat list

The agent has access to WebSearch, WebFetch, and Read only. **Playwright is not available to the agent** — if the agent reports failed URLs, you can retry them with Playwright after the agent returns (see Playwright Fallback below).

#### Research Instructions

The following applies to the agent (when delegated) or to you directly (when running inline).

Run 4–5 WebSearch queries. Do NOT site-lock queries — let search rank naturally, but prioritize results from the sources listed below. If your search tool supports geographic targeting (e.g., Brave Search's `country` parameter), scope queries to your country — `CA` for Canadian coverage.

#### Search Queries

1) `Canadian AI industry news {current month} {YYYY}` — broad sweep
2) `AI company funding investment acquisition Canada {current month} {YYYY}` — business moves
3) `AI jobs hiring growth Ontario Quebec Toronto Montreal {current month} {YYYY}` — labor & regional
4) `Canada AI policy regulation government {current month} {YYYY}` — policy angle
5) (Run only if queries 1–4 yield < 4 total items) `AI technology infrastructure data center Canada {YYYY}` — tech/infra backstop

#### Source Tiers

Prioritize results from these sources. The fetch strategy for each is based on tested accessibility — follow it exactly.

**Tier 1 — Canadian tech/AI primary sources (WebFetch these):**

| Source | Fetch Strategy | Notes |
|--------|---------------|-------|
| BetaKit (betakit.com) | Direct WebFetch | No paywall, clean full-text |
| The Logic (thelogic.co) | **Jina only** — `https://r.jina.ai/https://thelogic.co/...` | Direct fetch returns 403; Jina bypasses |
| CBC News Business (cbc.ca/news/business) | Direct WebFetch | Named journalists, no paywall |
| ISED Canada (ised-isde.canada.ca) | Direct WebFetch | Government policy docs and strategy |
| Canada.ca ISED press releases (canada.ca/en/innovation-science-economic-development) | Direct WebFetch | Government AI program announcements, funding awards |

**Tier 2 — Ecosystem & institutional sources (use search snippets unless substantive):**

| Source | Fetch Strategy | Notes |
|--------|---------------|-------|
| Vector Institute (vectorinstitute.ai) | Direct if needed | Institutional blog, Ontario AI ecosystem |
| Mila (mila.quebec/en/) | Direct if needed | Quebec AI ecosystem, use English URL |
| MaRS Discovery District (marsdd.com) | Direct if needed | Toronto startup ecosystem, editorial style |
| Invest Ontario (investontario.ca) | Direct if needed | FDI press releases, Ontario AI investment |

**Tier 3 — Global outlets with Canadian AI coverage (search snippets only):**

- TechCrunch
- VentureBeat
- Reuters / Bloomberg
- Indeed / LinkedIn economic reports

**Supplementary (use when discovered in results):**

- Investissement Quebec (investquebec.com) — primarily French; English content at `international.investquebec.com` requires Jina for SSL
- Bank of Canada (bankofcanada.ca) — AI economic analysis
- Maclean's (macleans.ca) — occasional AI features

#### WebFetch Rules

- **Cap at 6 WebFetch calls total** across all searches; prioritize the most substantive Tier 1 stories
- For The Logic: always prefix with `https://r.jina.ai/` — direct fetch will fail
- For any other source: if direct WebFetch fails or returns incomplete content, retry once with `https://r.jina.ai/{original-url}` (preserve original protocol)
- If Jina also fails, use the search snippet and move on
- Tier 2/3 sources: prefer search snippets; only WebFetch if the snippet is clearly incomplete and the story is important
- Skip paywalled or login-gated content — note the paywall, use whatever the snippet provides

#### Playwright Fallback (last resort)

If a URL fails both direct WebFetch and Jina, and the article is important enough to justify the overhead, try Playwright MCP tools. First attempt to load schemas via `ToolSearch` — if `ToolSearch` fails or the Playwright tools aren't available (MCP server not running), **skip Playwright entirely and use the search snippet.** Do not retry.

When Playwright is available, use ToolSearch (query: `+playwright browser`) to discover the correct tool names — they vary by plugin version and installation. You need four capabilities:

1) Navigate to a URL
2) Wait for article content to render
3) Capture/snapshot the page content
4) Close the browser

Cap at 2 Playwright fetches per run. If the first Playwright attempt itself fails (timeout, crash), abandon Playwright for the rest of the run.

#### Content Domains

**1. Funding, Investment & M&A**

- VC rounds, seed funding, Series A–D for Canadian AI companies
- Government grants and subsidies (IRAP, SR&ED, SDTC, provincial programs, AI Compute Access Fund)
- Acquisitions, mergers, IP licensing deals
- IPOs, SPACs, public market moves
- Foreign direct investment in Canadian AI (new offices, expansions)

**2. Jobs & Talent**

- Hiring surges, new office openings, team expansions at AI companies
- Layoffs and restructuring — report when newsworthy but don't let layoff stories dominate
- Immigration policy affecting AI talent (Express Entry, Global Talent Stream, tech-specific draws)
- Salary/compensation signals, labor market data
- University pipeline news (new AI programs, enrollment trends, co-op partnerships)
- **Notable hires**: Only include when the hire has meaningful industry implications — a leadership change that signals strategic direction, a high-profile move that reshapes a lab or company. Skip routine VP/director appointments unless the move tells a story about where the industry is heading.

**3. Company Growth & Market Moves**

- Canadian AI company expansions, new product launches, major partnerships
- Revenue milestones, customer wins, market entry/exit
- Startup ecosystem signals (accelerator cohorts, incubator news)
- Foreign AI companies entering the Canadian market

**4. Policy & Regulation**

- Federal AI legislation (AIDA successor, C-27 lineage, any new bills)
- Provincial policy: Ontario and Quebec AI strategies, funding programs, regulatory frameworks
- Government AI procurement and adoption (federal, provincial, municipal)
- Ethics frameworks, responsible AI initiatives
- Trade policy affecting AI (US-Canada tech relations, export controls)

**5. Research & Innovation** (secondary — include when commercially or policy-relevant)

- Breakthroughs from Canadian labs with commercial implications
- New open-source releases from Canadian companies or institutions
- Research partnerships between industry and academia

**6. Infrastructure & Compute** (secondary — include when newsworthy)

- Data center builds and cloud region launches in Canada
- Chip/hardware investments, semiconductor policy
- Compute access programs (academic, startup)

#### Exclude

- AI product tutorials or how-to guides
- Hype/doom opinion pieces without substantive news
- Global AI news with no Canadian angle
- Academic paper announcements without commercial or policy implications
- Conference talk summaries (unless announcing something newsworthy)

---

### Phase 4: Write the Note

**Path:** `<output-folder>/{YYYY-MM-DD}-canadian-ai-news.md`

#### Frontmatter

```yaml
---
title: "Canadian AI News - {YYYY-MM-DD}"
note-type: research
domain: [artificial-intelligence]
tags: [ai-industry, daily-digest, canada]
source: ["https://example.com/article-1", "https://example.com/article-2"]
---
```

The `source` array includes only URLs that were directly fetched (WebFetch or Playwright) — not snippet-only references.

#### Body

Use `##` headings for sections. **Skip any section that has no items** — do not include empty sections.

```markdown
## Funding, Investment & M&A

- **[Headline text](article-url)** — 2–3 sentence summary of the development and its significance. _Source · Region_

## Jobs & Talent

- **[Headline text](article-url)** — Summary. _Source · Region_

## Company Growth & Market Moves

- **[Headline text](article-url)** — Summary. _Source · Region_

## Policy & Regulation

- **[Headline text](article-url)** — Summary. _Source · Region_

## Research & Innovation

- **[Headline text](article-url)** — Summary. _Source · Region_

## Infrastructure & Compute

- **[Headline text](article-url)** — Summary. _Source · Region_
```

#### Geographic Tags

Each item's italicized footer includes a geographic tag after the source name:

- `· Ontario` — story primarily about Ontario / Toronto / Waterloo / Ottawa
- `· Quebec` — story primarily about Quebec / Montreal / Quebec City
- `· Canada` — federal scope, multi-provincial, or other provinces
- `· Alberta` / `· BC` / etc. — use specific province when applicable

#### Formatting Rules

- Each item: bold headline as markdown link (NOT wikilink — these are external URLs), dash separator, 2–3 sentence summary, source name + region in italics
- **3–7 items per section** — curated digest, not an exhaustive feed
- No `#` heading in body (reserved for title)
- Inline arrays in frontmatter (dash-separated multi-word values)
- If fewer than 3 noteworthy items found across ALL sections, add a line at the top of the note: `*Light news day — fewer developments than usual.*`
- If zero noteworthy items found, do not create the file — report that no developments were found and stop

#### Callouts

Use `[!quote]` for notable industry commentary — a sharp take or significant quote from an industry figure, policymaker, or researcher. Format:

```markdown
> [!quote] Speaker Name, Title — _Source_
> "The quoted text here."
```

- Maximum 1–2 per digest (only when genuinely notable)
- Place the callout directly after the item it relates to
- Do not use any other callout types
