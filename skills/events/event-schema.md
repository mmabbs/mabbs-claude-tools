## Event Schema & Note Template

### Common Event Schema (JSON)

Each scraper agent returns events in this format:

```json
[
	{
		"title": "Event Title",
		"date": "YYYY-MM-DD",
		"time": "HH:MM",
		"end_time": "HH:MM",
		"location": "Venue Name, Toronto, ON",
		"organizer": "Organizer Name",
		"url": "https://...",
		"source": "luma|meetup|eventbrite|techto|ai-tinkerers|vector",
		"category": ["tech"],
		"description": "One-line summary of the event",
		"tags": ["networking", "ai"]
	}
]
```

#### Field Rules

| Field       | Required | Notes                                                          |
| ----------- | -------- | -------------------------------------------------------------- |
| title       | yes      | Exact event title from source                                  |
| date        | yes      | ISO format YYYY-MM-DD                                          |
| time        | no       | 24h format HH:MM, null if unknown                              |
| end_time    | no       | 24h format HH:MM, null if unknown                              |
| location    | no       | Venue + city, "Online" for virtual, null if unknown            |
| organizer   | no       | Group or person hosting                                        |
| url         | yes      | Direct link to event page                                      |
| source      | yes      | One of: luma, meetup, eventbrite, techto, ai-tinkerers, vector |
| category    | yes      | Array of: tech, ai (at least one required)                     |
| description | no       | Max 2 sentences                                                |
| tags        | no       | Lowercase keywords (see Tag List below)                        |

#### Category Assignment

Each event gets at least one category. Events can belong to multiple.

| Category | Assign when the event involves...                                                                                   |
| -------- | ------------------------------------------------------------------------------------------------------------------- |
| tech     | Software dev, startups, SaaS, cloud, devops, data, product, design, fintech, cybersecurity, general tech networking |
| ai       | Artificial intelligence, machine learning, LLMs, generative AI, computer vision, NLP, AI ethics, AI applications    |

An "AI Startup Demo Day" gets `["tech", "ai"]`. A "Toronto Startup Pitch Night" gets `["tech"]`. When in doubt, include the category — over-tagging beats missing relevant events.

#### Tag List

Lowercase keywords for finer-grained filtering: networking, ai, startup, workshop, hackathon, social, career, dev, data, design, product, sales, health, fintech, crypto, security, devops, cloud, vr-ar, ml, llm, training, restricted

Apply `restricted` to events not open to the general public (sponsor-only, invite-only, members-only).

---

### Output Note Template

File path: `<output-path>/<city>-events-YYYY-MM-DD.md`

```markdown
---
title: <City> Events - {date}
scraped-date: { YYYY-MM-DD }
sources: [{ comma-separated sources that returned results }]
event-count: { total unique events }
categories: [{ categories with at least one event }]
---

## Tech Events

### {YYYY-MM-DD} — {Event Title}

- **Organizer**: {organizer}
- **Time**: {formatted time}
- **Location**: {location}
- **Source**: {Source Name}
- **Link**: [Details]({url})

> {description}

---

(repeat for each tech event, sorted by date then time)

## AI Events

(same format)

## Source Health

| Source           | Events  | Status                         |
| ---------------- | ------- | ------------------------------ |
| Meetup           | {count} | {OK or ⚠️ 0 events for N days} |
| Eventbrite       | {count} | ...                            |
| Luma             | {count} | ...                            |
| TechTO           | {count} | ...                            |
| AI Tinkerers     | {count} | ...                            |
| Vector Institute | {count} | ...                            |
```

#### Formatting Rules

- Time display: 12-hour format with AM/PM (e.g., "6:00 PM - 8:30 PM")
- If time unknown: omit the Time line
- If location unknown: omit the Location line
- If no description: omit the blockquote
- Horizontal rule `---` between events within a section
- Events sorted by date ascending, then time ascending within each category section
- **Omit empty category sections** — no heading if zero events in that category
- Events with multiple categories appear in each matching section (cross-listed)
- Events with the `restricted` tag: append " (restricted)" to the event title

#### Deduplication

Events are duplicates if they share:

- Same title (case-insensitive, trimmed) AND same date
- OR same URL

When deduplicating, prefer the source with more complete data. Merge fields from both if one has data the other lacks. Union category arrays from both records.
