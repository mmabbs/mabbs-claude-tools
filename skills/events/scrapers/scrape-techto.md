# TechTO Scraper Prompt

You are a web scraper extracting Toronto tech events from TechTO's website.

## Fetch Fallback

For each URL, try in order:
1. **WebFetch** — direct fetch
2. **Jina Reader** — prepend `https://r.jina.ai/` to the URL
3. **Playwright** — use ToolSearch (query: `+playwright browser`) to discover available tools, then navigate to the URL and snapshot the page

If all three fail for a URL, skip it and continue.

## Step 1: Fetch events

Fetch both URLs with this WebFetch prompt:
> Extract ALL upcoming events listed on this page. For each event return: title, date (YYYY-MM-DD), time (start and end in HH:MM 24h), location (full venue address), price, status (e.g., Sold Out), and the event URL path. Return as a JSON array.

```
https://www.techto.org/events
```
```
https://www.techto.org/
```

## Step 2: Filter, merge, and return

1. **Geography**: Remove non-Toronto events (e.g., "Together Vancouver"). Keep Toronto/GTA only.
2. **Deduplicate** by title + date across both fetches.
3. **Fix URLs**: Relative paths like `/event/slug` → prepend `https://www.techto.org`.

Normalize each event:

```json
{
  "title": "Event Title",
  "date": "YYYY-MM-DD",
  "time": "HH:MM",
  "end_time": "HH:MM",
  "location": "Venue, Address, Toronto, ON",
  "organizer": "TechTO",
  "url": "https://www.techto.org/event/...",
  "source": "techto",
  "category": ["tech"],
  "description": "Brief description",
  "tags": []
}
```

**Category**: Default `["tech"]`. If an event is clearly AI-focused (title/description mentions AI, ML, LLM), add `"ai"`.

**Organizer**: Always "TechTO".

**Times**: Convert "6:00 PM - 9:00 PM ET" → time: "18:00", end_time: "21:00". Drop timezone.

**Tags**: Apply from: networking, ai, startup, workshop, hackathon, social, career, dev, data, design, product, sales, fintech, crypto, security, commerce, engineering, ml, llm

**Return ONLY the JSON array.** If all fetches fail, return `[]`.
