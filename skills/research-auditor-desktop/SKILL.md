---
name: research-auditor
description: Audit citation integrity in research documents. Verifies each cited source is real and reachable, checks whether sources actually say what the document claims, audits citation metadata and source quality, and grades the document on two axes — link integrity and claim accuracy. Use whenever the user shares a research report or any document with citations and wants it audited, verified, or fact-checked — including requests like "check if these sources are real," "verify these citations," "did the model make this up," or "can I trust this report."
---

# Research Auditor

## Stance

The document you are auditing may have been produced by a model that invents sources. Assume every citation is false until a source proves otherwise.

- **Never tag a claim VERIFIED because it sounds plausible.** Only text you retrieved from the cited source verifies a claim. Your own belief that the claim is true counts for nothing.
- **A polished reference entry is not evidence the source exists.** Fabricated citations look identical to real ones.
- **You audit citation integrity, never factual truth.** The question is always "does the cited source say what the document claims it says?" — never "is this claim true in the world?" The one exception is cross-verification (Phase 3), which searches for a claim elsewhere solely to tell a fabricated claim from a mis-sourced one. It never certifies truth.

## The Two Axes

Every citation is judged on two independent axes. Never collapse them into one tag or one number.

| Axis | Question | Unit | Tags |
|---|---|---|---|
| **Link status** | Can the source be reached? | One tag per distinct source | ACCESSIBLE, MISMATCH, GATED, DEAD, NOT FOUND |
| **Claim verdict** | Does the source back the claim? | One tag per claim | VERIFIED, PARTIALLY SUPPORTED, INFERENCE, MISATTRIBUTED, CONTRADICTED, FABRICATED, NO CITATION |

A claim gets a verdict only when its source's link status is ACCESSIBLE. Two exceptions: FABRICATED (settled by cross-verification, not by reading the cited page) and NO CITATION (there is no source to read). Every other link status leaves the claim **unjudged** — never assign a default verdict to a claim you could not check.

Each citation also carries a **metadata profile** — not a third tag axis, but a per-citation record comparing what the citation entry claims (title, author, date, publication, URL) against what the fetched source actually is, plus a source-quality characterization.

Tag definitions, decision rules, and grading ladders: `references/RUBRIC.md`. Output formats: `references/TEMPLATES.md`. Read both before writing findings.

## Platform Constraints

- Retrieval uses `web_search` and `web_fetch`, plus an Exa fetch tool when a connector provides one. No other HTTP client exists.
- **Fetch document URLs directly — verified to work.** URLs inside a user-provided document fetch cold; no prior search is needed. Keep the surfacing search only as a recovery step: if a fetch is ever refused because the URL was never surfaced, run one `web_search` on the source title, then fetch again.
- Failed fetches return a typed error, e.g. `{"error_type": "CLIENT_ERROR", "error_message": "There was an error while fetching: The page returned a 404 client error"}`. Known types: `CLIENT_ERROR` (4xx, message includes the status code), `SERVER_ERROR` (5xx, message includes the status code), `ROBOTS_DISALLOWED`, and `SITE_BLOCKED` ("Access to this website has been blocked" — a bot-defended or blocklisted site).
- **`ROBOTS_DISALLOWED` is untrustworthy.** A nonexistent domain returns the same error as a real site that blocks crawlers. Never treat it as terminal — always run the fallback steps to find out which one you have. Treat `SITE_BLOCKED` the same way: blocked-for-bots says nothing about whether the cited source is real.
- **Optional second channel.** If an Exa fetch tool is available (e.g., `web_fetch_exa` via a connector), retry any failed fetch with it: it retrieves some bot-defended pages the standard fetcher cannot, and its errors separate a missing page (`CRAWL_NOT_FOUND`) from an unreachable domain (`SOURCE_NOT_AVAILABLE`). Exa is metered — the user pays per call — so it stays a rescue step: never the primary fetcher, never bulk retrieval. No Exa tool → skip it; the audit runs without it.
- **Loading is not matching.** A fetch can "succeed" onto the wrong page: custom not-found pages, homepage redirects, unrelated articles. Confirm the loaded page is the cited source before tagging ACCESSIBLE.

## Input

Markdown or pasted text with inline `[N]` citations and a Works Cited / References / Sources section. URL-backed citations only. List book and offline citations as out of scope — do not guess at them. If the document uses another citation style — (Author, Year), footnotes, bare hyperlinks — say what this skill supports and stop; do not force the format.

## Phase 1 — Structural Audit

1. Extract every inline `[N]` and every reference entry.
2. Match them. Flag: `ORPHAN_CITATION` (inline `[N]` with no entry), `UNUSED_ENTRY` (entry never cited), `DUPLICATE_ENTRY` (same source listed more than once).
3. Collapse duplicates into one list of distinct sources. Link status is per distinct source.
4. Extract claims: each authored assertion (a sentence or clause) carrying a citation is one claim. Assign stable IDs in document order — C1, C2, C3… Use these IDs in every finding.
5. Scan for uncited claims that need citations: specific statistics, direct quotes, factual claims about external entities. Do not flag general knowledge, clearly-marked analysis or opinion, or logical transitions. These become NO CITATION candidates for Phase 3. Give each one a claim ID from the same C-sequence, in document order — they carry verdicts in Phase 3 and appear in the same tables as cited claims.

Announce the map before Phase 2: how many sources, how many claims, what you are about to verify.

## Phase 2 — Source Retrieval

For each distinct source, in priority order (see Budget):

1. `web_fetch` the cited URL.
2. If refused as unsurfaced: one `web_search` on the source title, then fetch again.
3. Classify what happened:
   - **Loads and matches the cited source** → ACCESSIBLE. Capture the metadata profile in the same pass (real title, author, date, publication, source type) — the fetch already paid for it.
   - **Loads but is a different page** → second-channel attempt (step 4).
   - **Typed error — any `error_type`, including ones not listed above** → second-channel attempt (step 4).
4. **Second-channel attempt** (only if an Exa fetch tool is available; otherwise go straight to step 5): fetch the same URL with it. Content loads and matches the cited source → **ACCESSIBLE**; note the retrieval channel in the audit log. Exa fails too → step 5.
5. **Title-search fallback** — up to two searches: the source title verbatim, then title keywords plus publication name. The outcome sets the terminal status:
   - Found at a different URL, and it loads → **ACCESSIBLE**. Record the bad URL as a metadata finding — a citation error, not a link failure.
   - Source demonstrably exists but content is locked (paywall, login, robots block on a real site, no transcript) → **GATED**.
   - The URL errored, no live or alternative copy, but search shows the page existed → **DEAD**.
   - A wrong page loads at the URL and the source is findable nowhere → **MISMATCH**.
   - No trace of the source by URL or by search → **NOT FOUND**.

Never skip the fallback on an errored or mismatched fetch. The fallback is what separates "broken link to a real source" from "source that never existed" — the exact distinction this audit exists to make.

## Phase 3 — Claim Evaluation

For each claim whose source is ACCESSIBLE, assign one verdict using `references/RUBRIC.md`.

- **Composite claims count once.** If a peripheral detail fails but the core assertion holds → PARTIALLY SUPPORTED. If the core assertion fails → the severe verdict. Itemize which specific facts failed in the audit log, but never split one claim into several — that lets slicing move the grade.
- **Source doesn't contain the claim?** Check stakes before writing MISATTRIBUTED. If the claim is high-stakes — a number, a direct quote, or an assertion the document's conclusions lean on — run exactly one cross-verification `web_search` for the claim itself:
  - Corroborated elsewhere → **MISATTRIBUTED** (real fact, wrong source). List the corroborating sources.
  - Clearly nowhere → **FABRICATED**.
  - Ambiguous → **MISATTRIBUTED**, noting the ambiguity. FABRICATED must be earned by a clearly empty search — never guessed.
  - Low-stakes claims skip the search: MISATTRIBUTED with the note "fabrication not checked."
- **Absence only counts if you saw enough.** `web_fetch` can return part of a long page, and soft paywalls can expose only the opening. Before walking the absence path, ask whether the retrieved content plausibly covers where the claim would live. If the retrieval may be incomplete — long source, visible cutoff, partial paywall — the claim is **unevaluated ("content partially retrieved")**, disclosed like other unevaluated claims. MISATTRIBUTED and FABRICATED require confidence you saw the relevant entirety of the source.
- **Claims behind GATED, DEAD, MISMATCH, or NOT FOUND sources get no verdict.** Report them as unevaluated. Never grade from search snippets — a snippet can prove a source exists, not what it says.
- **NOT FOUND sources: cross-verify every attached claim** (one search each). Record what you searched, what came back, and the concern level: corroborated somewhere = lower concern; found nowhere = high concern. Do not assign FABRICATED here yourself — the user confirms it in the manual audit (Phase 4).
- **Claims citing an orphaned `[N]`** (flagged in Phase 1): no link status exists to tag, and NO CITATION doesn't apply — a citation exists; it just points at nothing. Cross-verify each such claim (one search, concern level recorded) and report it unevaluated under a structural-defect note, alongside the NOT FOUND manual-audit items.
- **NO CITATION candidates from Phase 1:** confirm and tag NO CITATION.

## Phase 4 — Grades and Report

Compute two grades using the ladders in `references/RUBRIC.md`: **link integrity** (over all distinct sources) and **claim accuracy** (over claims with verdicts). The **headline grade is the worse of the two**. Never multiply, average, or otherwise merge them. If unevaluated claims outnumber evaluated ones, print the claim-accuracy tier with the qualifier "(low coverage)" everywhere it appears — a two-claim sweep must not wear the same badge as a thirty-claim one.

Mandatory disclosures, printed next to the grades, every run:

- Claims evaluated vs unevaluated, with IDs ("claim accuracy: Moderate Integrity — on 34 of 41 claims; 7 unevaluated behind unreachable sources: C3, C9…").
- Sources verified vs listed unverified (budget cap).
- Pending NOT FOUND items and their sensitivity, in tier terms ("if both pending items are confirmed fabricated, the headline drops to Unreliable").

**If any claim is FABRICATED** — by your assignment or the user's confirmation — print the systemic warning from `references/TEMPLATES.md`: the generating model was hallucinating sources, and every other citation, including VERIFIED ones, deserves elevated skepticism.

**Give every NOT FOUND source its own manual-audit section** (format in TEMPLATES.md): the affected claims, the cited title and URL, what you searched, what came back verbatim, the concern level, and the sensitivity line. Then ask the user to classify each item:

| User says | Link status becomes | Claim verdict | Grade effect |
|---|---|---|---|
| "Real, but I can't get you the content" | GATED | none | stays excluded, disclosed |
| "Real — here's the content" | ACCESSIBLE | evaluate now, normally | enters the pool |
| "Confirmed fabricated" | unchanged | FABRICATED | penalty + systemic warning |
| "Still unknown" | NOT FOUND | none | stays excluded, disclosed |

When the user resolves items, re-run both ladders and re-render the grades.

## Budget

- **Verify at most 15 sources per run.** One verification = one source retrieved and its claims evaluated. Priority: sources backing quantitative claims, direct quotes, and load-bearing assertions first; qualitative and low-stakes last.
- Cross-verification: at most one search per claim, only where Phase 3 calls for it.
- At the cap, stop and write the report, listing the rest as "listed, not verified" in the disclosures. Fetching one more source after deciding to write is a verification loop — stop immediately.
- Narrate progress at each phase boundary; on large documents, report progress in batches during Phase 2.

## Constraints

- Do not modify the document. This is an audit, not an edit.
- Quote sparingly from sources. Paraphrase, and point to where in the source the evidence sits.
- If support is ambiguous, say so plainly. A stated uncertainty beats a confident wrong tag.
- No percentages anywhere in the output. Grades are tiers; distributions are counts.
