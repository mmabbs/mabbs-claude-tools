# Eventbrite Scraper Prompt

You are a web scraper extracting Toronto events from Eventbrite across tech and AI categories.

## Fetch Fallback

For each URL, try in order:
1. **WebFetch** — direct fetch
2. **Jina Reader** — prepend `https://r.jina.ai/` to the URL
3. **Playwright** — use ToolSearch (query: `+playwright browser`) to discover available tools, then navigate to the URL and snapshot the page

If all three fail for a URL, skip it and continue.

## Step 1: Fetch events by category

Fetch each URL with this WebFetch prompt:
> Extract ALL upcoming events from this page. For each event return a JSON object with: title, date (YYYY-MM-DD), time (HH:MM 24h), end_time (HH:MM 24h), location (venue + city), url (full eventbrite URL), description (1-2 sentence summary). Return as a JSON array.

**Tech events** (tag with `"category": ["tech"]`):
```
https://www.eventbrite.ca/d/canada--toronto/tech-meetup/
```
```
https://www.eventbrite.ca/d/canada--toronto/tech/
```

**AI events** (tag with `"category": ["ai"]`):
```
https://www.eventbrite.ca/d/canada--toronto/artificial-intelligence/
```

## Step 2: Filter, merge, and return

1. **Remove irrelevant events**: Kids camps, purely social clubs, music events. Keep: meetups, networking, workshops, conferences, hackathons, demo days, professional socials.

2. **Filter geography**: Keep events in the Toronto / GTA area.

3. **Deduplicate by URL** across all fetches. Union categories when an event appears in multiple fetches.

4. **Category refinement**: Review titles/descriptions — if it mentions AI/ML/LLM, add "ai".

Normalize each event:

```json
{
  "title": "Event Title",
  "date": "YYYY-MM-DD",
  "time": "HH:MM",
  "end_time": "HH:MM",
  "location": "Venue, Toronto, ON",
  "organizer": "",
  "url": "https://www.eventbrite.ca/e/...",
  "source": "eventbrite",
  "category": ["tech"],
  "description": "Brief description",
  "tags": []
}
```

Eventbrite doesn't always expose organizer names in listings — leave empty string if unknown.

**Tags**: Apply from: networking, ai, startup, workshop, hackathon, social, career, dev, data, design, product, sales, fintech, crypto, security, cloud, training, vr-ar, ml, llm

**Return ONLY the JSON array.** If all fetches fail, return `[]`.
