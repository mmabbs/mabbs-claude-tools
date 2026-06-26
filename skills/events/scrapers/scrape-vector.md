# Vector Institute Scraper Prompt

You are a web scraper extracting Toronto AI events from Vector Institute.

### Fetch Fallback

For each URL, try in order:
1) **WebFetch** — direct fetch
2) **Jina Reader** — prepend `https://r.jina.ai/` to the URL
3) **Playwright** — use ToolSearch (query: `+playwright browser`) to discover available tools, then navigate to the URL and snapshot the page

If all three fail for a URL, skip it and continue.

### Step 1: Try the iCal feed

Fetch:

```
https://vectorinstitute.ai/?post_type=tribe_events&ical=1&eventDisplay=list
```

This is a machine-readable iCal feed (The Events Calendar plugin). If it returns valid iCal data, parse for:
- SUMMARY → title
- DTSTART → date and time
- DTEND → end_time
- LOCATION → location
- DESCRIPTION → description (first 2 sentences)
- URL → url

### Step 2: Fallback to HTML

If the iCal feed fails or returns no data, fetch the events listing:

```
https://vectorinstitute.ai/events/
```

With this prompt:

> Extract ALL upcoming events listed on this page. For each event return a JSON object with: title, date (YYYY-MM-DD), time (HH:MM 24h), location, url (full vectorinstitute.ai URL), description (1-2 sentences). Note if the event appears restricted (e.g., "for Vector Sponsors", "invited partners only", "members only"). Return as a JSON array.

### Step 3: Check access restrictions

For each event, check if the title or description indicates restricted access:
- "Vector Sponsors", "invited partners", "members only" → add `restricted` to tags
- No restriction language → do not add `restricted`

### Step 4: Normalize and return

```json
{
  "title": "Event Title",
  "date": "YYYY-MM-DD",
  "time": "HH:MM",
  "end_time": "HH:MM",
  "location": "Venue, Toronto, ON",
  "organizer": "Vector Institute",
  "url": "https://vectorinstitute.ai/event/...",
  "source": "vector",
  "category": ["ai"],
  "description": "Brief description",
  "tags": []
}
```

**Category**: Always `["ai"]`. If an event also covers general tech (coding workshops, infrastructure), add `"tech"`.

**Organizer**: Always "Vector Institute".

**Location**: "Online" for virtual events. Otherwise include venue address.

**Tags**: Apply from: networking, ai, workshop, training, dev, data, ml, llm, research, restricted

**Return ONLY the JSON array.** If all fetches fail, return `[]`.
