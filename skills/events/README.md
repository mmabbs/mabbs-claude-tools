# events

A Claude Code skill that scrapes upcoming tech and AI events in Toronto from six sources, deduplicates them against previous runs, and writes a categorized Obsidian note.

The skill runs the full pipeline autonomously: parallel scraping across platforms, cross-source deduplication, source health tracking, and structured output — either interactively or on a daily cron schedule.

## What It Does

When triggered, the skill:

1. Checks if today's digest already exists (no duplicates)
2. Builds an exclusion list from all previous reports (no repeated events across days)
3. Launches 6 parallel scraper agents — one per source platform
4. Aggregates results: normalizes schemas, deduplicates within-run and cross-day, filters by keyword/date range
5. Writes a categorized note grouped by Tech Events and AI Events
6. Tracks source health — flags sources that return zero events for 3+ consecutive days

## Sources

| Source           | Platform                | Focus    | Scraper                                                   |
| ---------------- | ----------------------- | -------- | --------------------------------------------------------- |
| Luma             | luma.com                | tech, ai | [scrape-luma.md](scrapers/scrape-luma.md)                 |
| Meetup           | meetup.com              | tech, ai | [scrape-meetup.md](scrapers/scrape-meetup.md)             |
| Eventbrite       | eventbrite.ca           | tech, ai | [scrape-eventbrite.md](scrapers/scrape-eventbrite.md)     |
| TechTO           | techto.org              | tech     | [scrape-techto.md](scrapers/scrape-techto.md)             |
| AI Tinkerers     | toronto.aitinkerers.org | ai       | [scrape-ai-tinkerers.md](scrapers/scrape-ai-tinkerers.md) |
| Vector Institute | vectorinstitute.ai      | ai       | [scrape-vector.md](scrapers/scrape-vector.md)             |

Each scraper has its own fetch strategy tuned to the platform's behavior — which ones need Jina Reader to bypass 403s, which ones are SPAs requiring Playwright, which ones have iCal feeds. These are documented in the individual scraper files.

### Why Tiers?

The source list is split between general event platforms (Luma, Meetup, Eventbrite) and community-specific sources (TechTO, AI Tinkerers, Vector). General platforms cast a wide net but require aggressive filtering — a Toronto Luma search returns yoga classes and poetry readings alongside tech meetups. Community sources are pre-filtered by topic but have fewer events. Running both in parallel gives coverage without sacrificing signal quality.

## Sample Output

```markdown
---
title: Toronto Events - 2026-06-02
scraped-date: 2026-06-02
sources: [meetup, eventbrite, luma, techto, ai-tinkerers]
event-count: 14
categories: [tech, ai]
---

## Tech Events

### 2026-06-05 — Toronto Startup Pitch Night

- **Organizer**: TechTO
- **Time**: 6:00 PM - 9:00 PM
- **Location**: MaRS Discovery District, Toronto, ON
- **Source**: TechTO
- **Link**: [Details](https://www.techto.org/event/...)

> Monthly pitch night featuring 5 early-stage startups. Networking before and after.

---

### 2026-06-10 — Cloud Native Toronto Meetup

- **Organizer**: Cloud Native Toronto
- **Time**: 6:30 PM - 8:30 PM
- **Location**: Shopify Toronto, Toronto, ON
- **Source**: Meetup
- **Link**: [Details](https://www.meetup.com/...)

> Kubernetes best practices and service mesh deep-dive. Two lightning talks.

## AI Events

### 2026-06-12 — AI Tinkerers Toronto #24

- **Organizer**: AI Tinkerers Toronto
- **Time**: 6:00 PM - 9:00 PM
- **Location**: Burroughs Building, Toronto, ON
- **Source**: AI Tinkerers
- **Link**: [Details](https://toronto.aitinkerers.org/...)

> Monthly AI builder meetup. Demo night format — 5 builders show what they shipped.

## Source Health

| Source           | Events | Status                 |
| ---------------- | ------ | ---------------------- |
| Meetup           | 6      | OK                     |
| Eventbrite       | 4      | OK                     |
| Luma             | 3      | OK                     |
| TechTO           | 1      | OK                     |
| AI Tinkerers     | 1      | OK                     |
| Vector Institute | 0      | ⚠️ 0 events for 4 days |
```

## Usage

```
/events --output <output-folder>  # scrape all Toronto tech/AI events, next 30 days
/events --days 7                  # next 7 days only
/events --filter AI               # only events matching "AI"
```

The `--output` flag tells the skill where to write event notes and the `source-health.json` file. If omitted, the skill asks you for a path. There is no default — you decide where event notes belong in your project.

## Requirements

**Required:**

- Claude Code (CLI)
- Network access (WebFetch)

Each invocation spawns 6 parallel Sonnet agents (one per source). This runs comfortably within Pro plan rate limits but is worth knowing if you're on a metered plan.

**Optional — the skill works without these but gains capabilities with them:**

| Dependency                        | What it adds                                                                             | Without it                                                       |
| --------------------------------- | ---------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| Obsidian vault                    | Frontmatter metadata, vault-relative paths, daily note alerts, source health persistence | Outputs a plain markdown file; adapt paths and strip frontmatter |
| Playwright MCP                    | Last-resort fetch for SPAs that block standard requests (Luma, AI Tinkerers)             | Skipped automatically; Jina Reader handles most cases            |
| [Jina Reader](https://r.jina.ai/) | Fetch fallback for sites that block direct requests (free, no API key required)          | Falls through to Playwright or returns 0 events for that source  |
| Obsidian CLI                      | Daily note staleness warnings when a source goes stale                                   | Warnings appear in the summary output instead                    |

> **Playwright install note:** Use the Claude Code plugin system (`claude plugin install playwright`). Non-plugin MCP installations use different tool IDs — the scrapers discover tools via ToolSearch at runtime, but the `--allowedTools` flag in `events-scraper.sh` uses plugin-format tool names and may need updating for non-plugin setups.
>
> **Obsidian CLI** is a separate command-line tool for Obsidian vault operations — not part of the Obsidian app.

## Installation

```bash
# Clone and copy
git clone --depth 1 https://github.com/<user>/<repo>.git
cp -r <repo>/skills/events ~/.claude/skills/

# Optional: reduce permission prompts
# Add to .claude/settings.local.json:
# { "permissions": { "allow": ["WebFetch"] } }
```

### Headless / Cron Setup

The skill includes `events-scraper.sh` — a cron wrapper that runs the skill in headless mode. Configure the two variables at the top (`VAULT` and `CLAUDE_BIN`), then add to your crontab:

```bash
# Daily at 8 AM, weekdays only
0 8 * * 1-5 /path/to/events-scraper.sh
```

The script skips if today's note already exists and logs to `$HOME/.local/state/events-scraper/` (override with `EVENTS_LOG_DIR`).

## Adapting to Other Cities

The skill is built for Toronto, but the architecture is city-agnostic. To adapt:

1. **Scraper URLs** — Each file in `scrapers/` has hardcoded city URLs (e.g., Meetup's `location=ca--on--Toronto`, Eventbrite's `canada--toronto`). Replace with your city's equivalents.
2. **Luma** — Replace `luma.com/toronto` and `luma.com/discover?geo=Toronto` with your city's Luma page.
3. **Community sources** — TechTO, AI Tinkerers Toronto, and Vector Institute are Toronto-specific. Replace with your local equivalents, or remove them and add your own scraper files following the same pattern.
4. **Geographic filtering** — Update each scraper's geography filter to match your metro area.
5. **Output paths and titles** — Replace "Toronto Events" / `toronto-events-` with your city name in `event-schema.md` (note title), `SKILL.md` (the Step 0 glob and Step 3 write path), and `events-scraper.sh` (`NOTE_FILE`).

The event schema, deduplication logic, source health tracking, and output format are all city-agnostic — only the scraper URLs and names need changing.

## Adding or Removing Sources

To add a new source:

1. Create a new file in `scrapers/` following the existing pattern (intro, fetch fallback chain, fetch step, normalize step, return JSON array)
2. Add a row to the agent dispatch table in SKILL.md
3. The source will automatically appear in the Source Health table

To remove a source, delete its scraper file and remove its row from the dispatch table.

## Bundled Files

| File                                   | Purpose                                                                                 |
| -------------------------------------- | --------------------------------------------------------------------------------------- |
| [event-schema.md](event-schema.md)     | Shared event JSON schema, field rules, category definitions, and Obsidian note template |
| [events-scraper.sh](events-scraper.sh) | Cron wrapper for daily headless runs                                                    |
| [scrapers/](scrapers/)                 | Per-platform scraper prompts with tested fetch strategies                               |

## Notes for Non-Obsidian Users

The output includes Obsidian frontmatter and `> [!warning]` callout syntax for staleness alerts. If you're not using Obsidian, the frontmatter is harmless metadata, and the callouts render as plain blockquotes with visible `[!warning]` text. If you prefer no frontmatter, edit the output template in `event-schema.md`.
