---
name: events
disable-model-invocation: true
description: Scrape Toronto tech and AI events from multiple sources into a categorized markdown note with source-health tracking. Manual-only — invoke with /events (also handles scraper-health and source-status checks).
---

## Events Scraper

Scrape upcoming Toronto events across tech and AI communities. Produces a date-stamped, category-sectioned markdown note.

**Arguments:** `/events [--output <path>] [--filter keyword] [--days N]`

- `--output <path>` — Directory where event notes and health state are written (required on first run; ask the user if not provided)
- `--filter keyword` — Only include events whose title or description matches the keyword (case-insensitive)
- `--days N` — Only include events within the next N days (default: 30)
- No arguments — scrape all events for the next 30 days (prompts for output path if not previously set)

**City:** This skill ships configured for **Toronto**. To adapt to another city, see the README's "Adapting to Other Cities" section. The city name appears in filename patterns below as `<city>` — the shipped value is `toronto`.

---

### Pre-Flight

1) Read `event-schema.md` from this skill's directory — load the event schema and note template.
2) **Resolve output path** from `--output` argument. If not provided, ask the user: *"Where should event notes be written? Provide a directory path."* Do not assume a default — the user decides where these files belong.
3) Ensure the output directory exists (create it if needed).
4) Parse arguments for `--filter` and `--days` values.
5) Read source health file if it exists: `<output-path>/source-health.json`
6) Load Playwright MCP tool schemas via `ToolSearch` (query: `+playwright browser`). Scrapers use Playwright as a last-resort fetch fallback — loading schemas here avoids `InputValidationError` when an agent tries to call a deferred tool.

---

### Step 0: Load Previous Reports

Build a cumulative exclusion list from **all** previous reports to avoid re-listing events that were already covered. Single-predecessor comparison creates memory holes — events from two days ago reappear because they're not in yesterday's cleaned report.

```
Glob: <output-path>/<city>-events-*.md
```

Take **all** filenames by date prefix (excluding today's). For each, use **Grep** to extract:

- **URLs**: Lines matching `\[Details\]` — extract the URL from each `[Details](url)` link
- **Titles**: Lines matching `^### \d{4}-\d{2}-\d{2} —` — extract the date + title heading

These patterns must match the heading format and link text in `event-schema.md`. If you customize the note template, update these patterns accordingly.

Do **not** read the full files. Aggregate extracted URLs and title strings across all previous reports into a single **exclusion list**.

In Step 2, after within-run dedup, drop any event whose URL matches the exclusion list. Title+date matching is a fallback for events with different URLs across sources — it reliably catches same-source carryover but won't catch cross-source title variations (e.g., "AI Tinkerers #24" vs "AI Tinkerers Toronto #24"). URL-based dedup handles the primary case.

If no previous reports exist, proceed without an exclusion list.

---

### Step 1: Parallel Source Scraping

Launch **6 parallel agents** (subagent_type: `general-purpose`, model: `sonnet`). Each agent gets the prompt from its corresponding template file in this skill's directory.

Read each prompt template before dispatching:

| Source | Prompt File | Category Focus |
|--------|-------------|----------------|
| Luma | `scrapers/scrape-luma.md` | tech, ai |
| Meetup | `scrapers/scrape-meetup.md` | tech, ai |
| Eventbrite | `scrapers/scrape-eventbrite.md` | tech, ai |
| TechTO | `scrapers/scrape-techto.md` | tech |
| AI Tinkerers | `scrapers/scrape-ai-tinkerers.md` | ai |
| Vector Institute | `scrapers/scrape-vector.md` | ai |

Dispatch all 6 in a **single message** so they run concurrently. Each agent returns a JSON array of events matching the schema in `event-schema.md`.

---

### Step 2: Aggregate Results

After all agents return:

1) **Parse** each agent's response — extract the JSON array. If the response is wrapped in markdown code fences, strip them before parsing. If an agent failed or returned no events, log it and continue with the others.

2) **Normalize** — Ensure all events conform to the schema:
   - Dates in YYYY-MM-DD format
   - Times in HH:MM 24-hour format
   - Source field set correctly
   - Category is a non-empty array of valid values (tech, ai)

3) **Deduplicate (within-run)** — per the rules in `event-schema.md` (same title+date or same URL). Prefer the record with more complete fields. Union category arrays from duplicates.

4) **Deduplicate (cross-day)** — Drop any event whose URL appears in the exclusion list from Step 0. For events without a URL match, drop if the title+date heading matches an exclusion list entry. Log the count of excluded events for the Step 6 summary.

5) **Filter** (if `--filter` provided) — Keep only events where title or description contains the keyword (case-insensitive).

6) **Date range** (if `--days` provided, default 30) — Keep only events within the next N days from today.

7) **Sort** — By date ascending, then time ascending.

---

### Step 3: Write Note

1) Read the note template from `event-schema.md`.
2) Generate the note with:
   - Frontmatter per the template (scraped-date, sources, event-count, categories)
   - **Category sections**: Group events by category. Events with multiple categories appear in each matching section. Omit sections with zero events.
   - **Source Health table** at the end
3) Write to: `<output-path>/<city>-events-YYYY-MM-DD.md`
   - Same-day re-runs overwrite the previous scrape.

---

### Step 4: Update Source Health

Read and update `<output-path>/source-health.json`:

```json
{
  "meetup": {"last_success": "2026-05-19", "zero_streak": 0},
  "eventbrite": {"last_success": "2026-05-19", "zero_streak": 0},
  "luma": {"last_success": "2026-05-17", "zero_streak": 2}
}
```

For each source, use the **raw event count from Step 1** (before dedup, filter, or date-range):
- Returned >0 events → set `last_success` to today, reset `zero_streak` to 0
- Returned 0 events → increment `zero_streak` by 1

Include the Source Health table in the note. Flag any source with `zero_streak >= 3` with a ⚠️ warning.

---

### Step 5: Daily Note Alert

If any source has `zero_streak >= 3`, append a staleness warning to today's daily note under `## Notes`:

```
> [!warning] Events scraper: {source} returned 0 events for {N} consecutive days. Scraper may need attention.
```

Use the CLI command: `obsidian daily:append "{warning text}"`

If the Obsidian CLI isn't available (no vault, or running standalone), surface the warning in the Step 6 summary instead.

---

### Step 6: Summary (interactive only)

When run interactively (not via cron), report:

- Events found per source (before dedup)
- Events after dedup, by category
- Events filtered out (if `--filter` used)
- Final event count and file path
- Any failed sources and staleness warnings

---

### Error Handling

- Agent timeout/failure: log the error, continue with other sources.
- ALL sources fail: do not write an empty note. In interactive mode, inform the user. In headless mode, append a warning to the daily note.
- **Zero events after processing**: If all sources succeed but 0 events remain after dedup, filtering, and date-range checks — do not write an empty note. Append to today's daily note under `## Notes`:

  ```
  > [!warning] Events scraper ran but found 0 upcoming events after filtering. Sources were healthy — no new events in the next {N} days.
  ```

  Use the CLI command: `obsidian daily:append "{warning text}"`
- Each scraper prompt includes a fetch fallback chain (WebFetch → Jina Reader → Playwright). Scrapers handle this internally.
- Unparseable data counts as 0 events for that source.

