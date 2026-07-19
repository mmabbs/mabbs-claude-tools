# Evaluation Rubric

Tag definitions, decision rules, and grading ladders. Read fully before assigning any tag.

Contents:

1. Link status tags
2. Fetch-error handling
3. Claim verdict tags
4. Verdict decision order
5. Composite and multi-source claims
6. Citation metadata profile
7. Source quality characterization
8. Grading ladders
9. Edge cases

## 1. Link Status Tags

One tag per distinct source. Describes whether the source could be reached — nothing else. Never let a link tag imply anything about claim accuracy.

| Tag | Meaning | Suspicion |
|---|---|---|
| ACCESSIBLE | Content retrieved and confirmed to be the cited source | None |
| MISMATCH | A page loads at the URL, but it is not the cited source, and the source is findable nowhere else | High — a decoy URL is a hallucination signature |
| GATED | Source demonstrably exists; content locked (paywall, login, robots block on a real site, video/podcast without transcript, unparseable format) | Low |
| DEAD | The URL errors, no live or alternative copy found, but search shows the page existed | Moderate |
| NOT FOUND | No trace of the source by URL or by title/keyword search | Highest |

- **ACCESSIBLE requires an identity check.** The loaded page's title and publication must match the citation. "Something loaded" is not ACCESSIBLE.
- **MISMATCH is terminal only after the fallback fails.** If the title search finds the real source elsewhere, the status is ACCESSIBLE and the bad URL is a metadata finding.
- **NOT FOUND is a pending state, not a conviction.** It goes to the user's manual audit. Only the user's confirmation turns it into fabrication.
- **Partial retrieval behaves like GATED for the claims it hides.** When identity is confirmed but the retrieved content is incomplete — truncated fetch, soft paywall — claims whose evidence would sit in the missing portion are unevaluated ("content partially retrieved"), never MISATTRIBUTED. Absence from retrieved text equals absence from the source only when you saw the relevant entirety.

## 2. Fetch-Error Handling

Failed fetches return `{"error_type": ..., "error_message": ...}`. Map them:

| error_type | What it tells you | What to do |
|---|---|---|
| `CLIENT_ERROR` (message includes the 4xx code) | Page is not there now | Title-search fallback |
| `SERVER_ERROR` (message includes the 5xx code) | Server failing, possibly temporarily | Retry the fetch once, then fallback |
| `ROBOTS_DISALLOWED` | Ambiguous: a real site blocking crawlers OR a nonexistent domain — the tool reports both identically | Never terminal. Fallback decides: source found to be real → GATED; no trace → NOT FOUND |
| `SITE_BLOCKED` | Access blocked — bot defense or blocklist. Says nothing about whether the cited source is real | Never terminal. Second-channel fetch if available, then fallback |
| anything else | Unknown failure | Second-channel fetch if available, then title-search fallback |

**An error type alone never sets a terminal status.** Terminal status = error type + fallback outcome. This is the rule that keeps a hallucinated domain from hiding behind a polite-looking "site disallows automated access" message.

### Second-channel (Exa) errors

When an Exa fetch tool is available, its failures use a different taxonomy:

| Exa error | What it suggests | Weight |
|---|---|---|
| `CRAWL_NOT_FOUND` | Page missing (404-equivalent) | Corroborates a `CLIENT_ERROR` from the standard fetcher |
| `CRAWL_LIVECRAWL_TIMEOUT` | Fetch timed out — also observed on 5xx server errors | Retrieval failure only; proves nothing about the source |
| `SOURCE_NOT_AVAILABLE` | Domain unreachable | Strong — but not conclusive — signal the domain doesn't exist |

Channels agreeing is evidence. Standard fetch `ROBOTS_DISALLOWED` + Exa `SOURCE_NOT_AVAILABLE` + an empty title search = a confident NOT FOUND. The title search still makes the final call; the second channel sharpens it.

## 3. Claim Verdict Tags

One verdict per claim (per authored assertion, ID'd C1…Cn). Rendered only when the source is ACCESSIBLE — except FABRICATED and NO CITATION.

### VERIFIED

Source states the claim with matching meaning and scope.

Criteria (all must hold):

- Source explicitly states the fact, statistic, or conclusion
- Claim scope matches source scope — no overgeneralization
- Quantities match within reasonable rounding
- Attribution is accurate

> Report: "73% of surveyed households reduced their energy use in 2024"
> Source: "73% of households reduced energy consumption in 2024"
> → VERIFIED

### PARTIALLY SUPPORTED

Directionally right, but overstated, understated, narrower, or broader than the source.

Criteria (any):

- Source says "some/many," claim says "most/all"
- Source gives a range, claim cherry-picks an end
- Source discusses a related but not identical topic
- Magnitude differs meaningfully
- Source's caveats dropped

> Report: "Remote workers are more productive than in-office workers"
> Source: "Remote workers self-reported higher productivity on focused, individual tasks"
> → PARTIALLY SUPPORTED — true for self-reported focused tasks, not productivity overall

### INFERENCE

Derivable from the source, but the source does not say it outright. The citation implies direct support; the actual support is a derivation. Score it — the user decides whether the leap was warranted.

Criteria:

- Follows from the source's data
- A reasonable reader could draw it
- Not a significant leap (a leap that lands somewhere the source doesn't point → MISATTRIBUTED)

> Report: "This points to growing public support for the policy"
> Source: Polls show approval rose from 41% to 58% over two years
> → INFERENCE — reasonable reading of the trend, not a stated conclusion

### MISATTRIBUTED

The source does not contain the claim — and the claim is not shown to be invented. Either it was corroborated elsewhere (real fact, wrong source), or fabrication wasn't checked (low-stakes claim, search skipped) — say which in the finding.

> Report: "The city's transit ridership grew 30% last year" [cites source A]
> Source A: reports a 30% rise in *cycling* trips; says nothing about transit
> → MISATTRIBUTED — the figure belongs to a different metric

### CONTRADICTED

The source states the opposite of the claim, or the claim inverts the source's conclusion.

> Report: "Transit ridership grew 30% last year"
> Source: reports ridership *declined* for the third consecutive year
> → CONTRADICTED

### FABRICATED

The claim appears invented: the cited source does not support it AND one cross-verification search finds it nowhere.

Exactly two routes to this verdict — no others:

1. ACCESSIBLE source + claim absent + high-stakes + clearly empty cross-verification search → assign it.
2. NOT FOUND source + the user confirms fabrication in the manual audit → assign it.

Never assign FABRICATED from a hunch, a skipped search, or an ambiguous search. If in doubt, MISATTRIBUTED with a note. FABRICATED is the audit's most severe verdict; it must be earned.

### NO CITATION

A claim that needs a citation and has none.

Flag: specific statistics, direct quotes, factual claims about external entities, claims about what others said or did, controversial assertions.
Don't flag: general knowledge, clearly-marked analysis or opinion, logical transitions.

## 4. Verdict Decision Order

For a claim with an ACCESSIBLE source, walk down and stop at the first match:

1. Source states the opposite → CONTRADICTED
2. Source states it, meaning and scope match → VERIFIED
3. Source states something directionally similar but off in scope or magnitude → PARTIALLY SUPPORTED
4. Source implies it derivably → INFERENCE
5. Source doesn't contain it → MISATTRIBUTED or FABRICATED, per the cross-verification rules (SKILL.md Phase 3)

## 5. Composite and Multi-Source Claims

- **Composite claim, mixed results:** the claim counts once. Core assertion holds, peripheral detail fails → PARTIALLY SUPPORTED. Core assertion fails → the severe verdict (CONTRADICTED, MISATTRIBUTED, or FABRICATED). Itemize the atomic facts that failed in the audit log — the log gets the detail, the grade gets one unit.
- **One claim, multiple citations:** judge against all cited sources. VERIFIED if at least one fully supports and none contradicts. If the cited sources disagree with each other, note the conflict — the claim cannot be VERIFIED.
- **One citation, multiple claims:** judge each claim separately.
- **Synthesis across sources:** if the synthesized conclusion is not stated in any single cited source → INFERENCE at best.

## 6. Citation Metadata Profile

Populate for every source whose content you retrieved — including sources recovered from a bad URL via the fallback. Skip when no source was found: you cannot validate a bibliographic record against something that doesn't exist. That situation is NOT FOUND on the link axis and possibly fabrication on the claim axis — not a metadata error.

Compare each field independently; report each mismatch as its own discrete finding:

| Field | Report as |
|---|---|
| Title | exact / paraphrased / wrong |
| Author | correct / wrong / missing |
| Date | correct / wrong / missing |
| Publication | correct / wrong |
| URL | correct / wrong-but-source-real (recovered via fallback) |

Wrong author, invented URL path, and wrong publication are major findings. A paraphrased title is minor. Multiple metadata errors on one citation compound suspicion — call out the pattern when you see it.

## 7. Source Quality Characterization

For every ACCESSIBLE source, characterize provenance. This is a call you make, not one you defer.

- **Type:** peer-reviewed / institutional (government, academic, standards body) / independent journalism / trade press / corporate material or press release / self-published (blog, newsletter) / user-generated (forum, wiki).
- **Independence:** flag self-interested sourcing plainly. A claim about an entity backed by that entity's own material — "Company X leads the market" cited to Company X's press release — is self-interested sourcing. Say so.
- **Representation:** flag provenance mismatch. Content framed as research or reporting but backed by an uncredentialed or self-published source is a mismatch. Say so.

Boundary: characterize and flag; never rule a source "adequate" or "inadequate" for a specific claim. The user decides what to do with the characterization.

## 8. Grading Ladders

No percentages, no decimals. Four tiers: **High Integrity / Moderate Integrity / Significant Concerns / Unreliable.** Walk each ladder top-down; the first matching rule sets the grade.

### Link integrity

Denominator: all distinct sources. Nothing is ever excluded from this axis.

1. Failure statuses (MISMATCH + DEAD + NOT FOUND) outnumber ACCESSIBLE sources → **Unreliable**
2. Any NOT FOUND or MISMATCH → **Significant Concerns**
3. Any DEAD → **Moderate Integrity**
4. Every source ACCESSIBLE or GATED → **High Integrity**

GATED never caps this grade — a paywalled real source is not a citation failure. Its cost shows up in the unevaluated-claims disclosure instead.

### Claim accuracy

Denominator: claims with verdicts — evaluated claims plus FABRICATED plus NO CITATION. Unevaluated claims (behind unreachable or gated sources) are excluded from the math and **always disclosed** next to the grade, with IDs. Their access failure is already counted once, on the link axis — counting it here too would punish it twice; hiding it would repeat the old subset-hiding bug. Disclosure is the escape. When unevaluated claims outnumber evaluated ones, print the tier with the qualifier "(low coverage)" — a count rule, not a percentage.

1. Any FABRICATED → **Unreliable** (and print the systemic warning)
2. Severe verdicts (MISATTRIBUTED + CONTRADICTED + NO CITATION) outnumber VERIFIED → **Unreliable**
3. Any CONTRADICTED → **Significant Concerns**
4. Any MISATTRIBUTED or NO CITATION → **Moderate Integrity**
5. Only VERIFIED / PARTIALLY SUPPORTED / INFERENCE remain: VERIFIED outnumber the other two combined by at least four to one → **High Integrity**; otherwise → **Moderate Integrity**

### Headline

The worse of the two tiers. Always show three lines — link integrity, claim accuracy, headline — plus the disclosures. Never merge the axes into a single number: fusing access failures with accuracy failures is the exact defect this design replaced. (A future logic-audit grade joins as its own fourth line under the same rule — worst tier wins, and no grade ever feeds another grade's computation.)

### Sensitivity for pending items

While NOT FOUND items await the user's manual audit, state what their resolution could do — in tier terms, never percentages. Method: re-run both ladders hypothetically with every pending item as confirmed FABRICATED, and report the result ("if both pending items are confirmed fabricated, the headline drops to Unreliable").

## 9. Edge Cases

- **Self-citations** (the document cites its own author or organization): flag for review, don't auto-reject.
- **Redirects** that land on the right content: ACCESSIBLE.
- **Soft 404s** — a "page not found" page that loads successfully: not ACCESSIBLE. Treat as a failed fetch and run the fallback.
- **Archived copies** (Wayback Machine and similar): if an archived copy loads and matches, evaluate claims against it — link status ACCESSIBLE, with a metadata note "live URL dead; evaluated against archived copy."
- **Second-channel retrievals:** when Exa fetched what the standard fetcher couldn't, the source is ACCESSIBLE — note the channel in the audit log.
- **Rate limits mid-audit:** a constraint on the audit run, not a property of any source. Batch, tell the user, resume. Never let the audit's own limits set a source's tag.
