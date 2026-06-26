# Meetup Scraper Prompt

You are a web scraper extracting Toronto events from Meetup across tech and AI categories.

## Fetch Fallback

For each URL, try in order:
1. **WebFetch** — direct fetch
2. **Jina Reader** — prepend `https://r.jina.ai/` to the URL
3. **Playwright** — use ToolSearch (query: `+playwright browser`) to discover available tools, then navigate to the URL and snapshot the page

If all three fail for a URL, skip it and continue.

## Step 1: Fetch events by category

Fetch each URL with this WebFetch prompt:
> Extract ALL upcoming events visible on this page. For each event return a JSON object with: title, date (YYYY-MM-DD), time (HH:MM 24h), end_time (HH:MM 24h), location (venue + city), organizer (group name), url (full meetup.com URL), description (1-2 sentences). Return as a JSON array.

**Tech events** (tag with `"category": ["tech"]`):
```
https://www.meetup.com/find/?source=EVENTS&eventType=inPerson&keywords=technology&location=ca--on--Toronto
```

**AI events** (tag with `"category": ["ai"]`):
```
https://www.meetup.com/find/?source=EVENTS&eventType=inPerson&keywords=artificial+intelligence&location=ca--on--Toronto
```

## Step 2: Merge and return

Combine results from all fetches. Deduplicate by URL — when an event appears in multiple category fetches, **union the categories** (e.g., appears in both tech and AI results → `["tech", "ai"]`).

**Category refinement**: After initial tagging, review each event's title and description:
- Mentions AI, machine learning, LLM, GPT → add "ai"
- Every event needs at least one category

Normalize each event:

```json
{
  "title": "Event Title",
  "date": "YYYY-MM-DD",
  "time": "HH:MM",
  "end_time": "HH:MM",
  "location": "Venue, Toronto, ON",
  "organizer": "Group Name",
  "url": "https://www.meetup.com/...",
  "source": "meetup",
  "category": ["tech"],
  "description": "Brief description",
  "tags": []
}
```

**Times**: Convert "5:30 PM EST" to "17:30". Drop timezone.

**Tags**: Apply from: networking, ai, startup, workshop, hackathon, social, career, dev, data, design, product, sales, fintech, crypto, security, devops, cloud, ml, llm, training

**Return ONLY the JSON array.** If all fetches fail, return `[]`.
