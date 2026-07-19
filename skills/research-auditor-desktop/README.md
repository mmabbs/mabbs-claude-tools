# research-auditor

A skill that audits citation integrity in research documents — especially LLM-generated research. It verifies that cited sources are real and reachable, checks whether each source actually says what the document claims, audits citation metadata and source quality, and grades the document on two independent axes.

This is the **Desktop / claude.ai variant**: it runs on the `web_search` + `web_fetch` retrieval surface. That's why the repo folder is named `research-auditor-desktop`.

> **Scope**: Built for and tested against Claude's research output. It may work on research from other LLMs, but citation patterns and failure modes differ across models — transferability is not tested or guaranteed.

## What It Does

Give it a research document with `[N]` inline citations and a references section, and it runs a four-phase audit:

1. **Structural audit** — extracts every inline citation and reference entry, matches them (flagging orphans, unused entries, and duplicates), assigns stable IDs to every cited claim, and scans for claims that need citations but have none.
2. **Source retrieval** — fetches each distinct source through a fallback ladder (direct fetch → surfacing search → optional Exa second channel → title-search fallback) and assigns one of five link-status tags. The ladder exists to separate "broken link to a real source" from "source that never existed."
3. **Claim evaluation** — for each claim behind a reachable source, assigns one of seven verdicts against the bundled rubric. High-stakes unsupported claims get one cross-verification search to tell a mis-sourced fact from a fabricated one.
4. **Grades and report** — computes two tier grades, prints mandatory disclosures, and hands sources it can't locate anywhere to you for a manual-audit call.

## Sample Output (abbreviated)

```markdown
## Grades

| Axis | Grade | Basis |
|---|---|---|
| Link integrity | Significant Concerns | 9 of 12 sources accessible; 1 GATED, 1 DEAD, 1 NOT FOUND |
| Claim accuracy | Moderate Integrity | over 18 claims with verdicts; capped by 1 MISATTRIBUTED |
| **Headline** | **Significant Concerns** | worse of the two axes |

**Disclosures**:
- Claims evaluated: 17 of 21. Unevaluated behind unreachable/gated sources: 3 (C7, C15, C16).
- Sources verified: 12 of 12.
- Pending manual audit: 1 NOT FOUND source.
  Sensitivity: if the pending item is confirmed fabricated, the headline drops to Unreliable.
```

Each NOT FOUND source then gets its own manual-audit section — cited URL, verbatim fetch error, searches already run, affected claims, concern level — and the grades re-render after you classify it. The full report format lives in [references/TEMPLATES.md](references/TEMPLATES.md).

## The Two-Axis Model

The skill's core design decision: reachability and accuracy are different failures, so they never share a tag set or a score.

**Link status** — one tag per distinct source. Can it be reached?

| Tag | Meaning |
|---|---|
| `ACCESSIBLE` | Content retrieved and confirmed to be the cited source |
| `MISMATCH` | A page loads, but it's not the cited source — and the source is findable nowhere else |
| `GATED` | Source exists; content locked (paywall, login, robots block) |
| `DEAD` | URL errors; no live copy, but evidence the page existed |
| `NOT FOUND` | No trace of the source by URL or by search |

**Claim verdict** — one tag per claim. Does the source back it?

| Tag | Meaning |
|---|---|
| `VERIFIED` | Source states the claim, matching meaning and scope |
| `PARTIALLY SUPPORTED` | Directionally right but overstated, understated, or scope-shifted |
| `INFERENCE` | Derivable from the source, but not stated outright |
| `MISATTRIBUTED` | Source doesn't contain the claim (the claim may be real, just mis-sourced) |
| `CONTRADICTED` | Source states the opposite |
| `FABRICATED` | Claim appears invented — unsupported by the cited source and corroborated nowhere |
| `NO CITATION` | A claim that needs a citation and has none |

Claims behind unreachable sources are never graded and never silently dropped — they're excluded from the accuracy math and always disclosed by ID next to the grade. Every citation also gets a metadata profile (cited title/author/date/publication/URL vs. what the source actually is) and a source-quality characterization (provenance type, independence flags).

## Grading

No percentages. Two tier grades — **link integrity** and **claim accuracy** — on a four-tier ladder (High Integrity / Moderate Integrity / Significant Concerns / Unreliable), driven by severity caps: any FABRICATED claim floors the grade and triggers a document-wide systemic warning; CONTRADICTED and MISATTRIBUTED impose their own ceilings. The headline grade is simply the **worse of the two axes** — the design guarantees a report can't hide dead links behind accurate surviving claims, or vice versa.

Sources the skill can't locate at all go to a **manual audit workflow**: each NOT FOUND item is handed to you with the searches already run, a concern level (claim corroborated elsewhere vs. found nowhere), and a sensitivity line ("if this is confirmed fabricated, the headline drops a tier"). You classify each item; the skill re-renders the grades.

## How Retrieval Works

The skill's retrieval surface uses `web_search` and `web_fetch`:

- Sources are fetched with `web_fetch`, attempted directly on each cited URL (URLs in a user-provided document fetch cold — no prior search needed), with a `web_search` surfacing step as a recovery path if a fetch is refused.
- Failed fetches return typed errors (`CLIENT_ERROR`, `SERVER_ERROR`, `ROBOTS_DISALLOWED`, `SITE_BLOCKED`). Notably, a nonexistent domain and a crawler-blocking real site return the *same* `ROBOTS_DISALLOWED` error — so the skill never trusts blocked-access errors alone and always disambiguates with a title search.
- If an Exa fetch connector is available, the skill uses it as an optional second channel: it retrieves some bot-defended pages the standard fetcher can't, and its error taxonomy separates a missing page from an unreachable domain. Exa is a metered API, so the skill reaches for it only to rescue failed fetches — a few calls per audit, never bulk retrieval. Without Exa, the audit runs single-channel — nothing else changes.
- There is no `curl`/`pandoc` pre-fetch workflow here; the audit fetches sources live during the run.

**Honest expectations:** the typed-error taxonomy above is empirically observed behavior of Claude's fetch tooling (as of July 2026), not a documented contract — it can change without notice. If the error types drift, the retrieval ladder still works; only the error-mapping table in `references/RUBRIC.md` may need updating.

## Requirements

| Component | Required? | Without it |
|---|---|---|
| Claude with Skills enabled (Desktop, claude.ai) | Required | Nowhere to run — this variant targets the `web_search`/`web_fetch` surface |
| Web access (`web_search` + `web_fetch`) | Required | No retrieval — the audit cannot verify anything |
| Exa fetch connector (e.g. `web_fetch_exa`) | Optional | Single-channel retrieval: some bot-defended pages can't be rescued, and the missing-page vs. unreachable-domain signal is coarser. Nothing else changes |
| Input: Markdown or pasted text with `[N]` inline citations and a Works Cited / References section, URL-backed | Required (format) | Book and offline citations are listed as out of scope — never guessed at |

## Installation

1. Download or clone this folder (`research-auditor-desktop`).
2. **Rename your copy of the folder to `research-auditor`.** The folder name inside the ZIP must match the `name` field in SKILL.md frontmatter — Anthropic's skill packaging docs state this as a hard requirement, and a mismatch fails upload.
3. Optionally delete this `README.md` from your copy — it's repo documentation, not skill content, and Anthropic's packaging guide recommends skill folders carry only SKILL.md and its references.
4. ZIP the renamed folder (the folder goes inside the ZIP — not its files at the ZIP root).
5. Upload via Settings → Capabilities → Skills. See [Anthropic's skill documentation](https://support.claude.com/en/articles/12512180-use-skills-in-claude) for the full flow.

The skill triggers when you ask Claude to audit, verify, or fact-check citations in a research document you've shared.

## Bundled References

| File | Purpose |
|---|---|
| [references/RUBRIC.md](references/RUBRIC.md) | Tag definitions, fetch-error handling, verdict decision order, metadata profile, source-quality characterization, grading ladders, edge cases |
| [references/TEMPLATES.md](references/TEMPLATES.md) | Output formats: executive summary, systemic warning, critical findings, manual-audit sections, full audit log |

## Changelog

### 2026-07-19

- First public release: four-phase audit, two-axis tagging and grading, manual-audit workflow for unlocatable sources, optional Exa second channel.
- Post-review fixes from an adversarial critique run: partial-content guard (a claim absent from a possibly-truncated retrieval is unevaluated, never MISATTRIBUTED/FABRICATED), orphan-citation protocol (cross-verify and disclose, mirroring NOT FOUND handling), "(low coverage)" qualifier on the claim-accuracy tier when unevaluated claims outnumber evaluated ones, graceful rejection of unsupported citation styles, out-of-scope slot in the report template, and uncited claims now share the C-ID sequence.
