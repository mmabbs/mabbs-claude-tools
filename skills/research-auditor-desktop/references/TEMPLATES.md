# Citation Audit Output Templates

Use these structures exactly. Counts, tiers, and claim IDs everywhere — never percentages.

## Executive Summary

```markdown
# Citation Audit Report

**Document**: [Title]
**Audit date**: [Date]
**Sources**: [N] distinct ([M] reference entries; [k] duplicates collapsed; [j] out of scope — book/offline)
**Claims**: [N] claims under audit, IDs C1–C[N] in document order ([k] with citations, [m] uncited findings)

## Grades

| Axis | Grade | Basis |
|---|---|---|
| Link integrity | [tier] | [n] of [N] sources accessible; [list failure counts, e.g. "1 DEAD, 2 NOT FOUND"] |
| Claim accuracy | [tier] | over [n] claims with verdicts; [rule that set the tier, e.g. "capped by 1 MISATTRIBUTED"] |
| **Headline** | **[worse tier]** | worse of the two axes |

**Disclosures** (never omit):
- Claims evaluated: [n] of [N]. Unevaluated behind unreachable/gated sources: [m] ([IDs]).
- Sources verified: [n] of [N]. Listed unverified (budget cap): [m].
- Pending manual audit: [k] NOT FOUND source(s) — see Manual Audit below.
  Sensitivity: [tier-terms statement, e.g. "if both pending items are confirmed fabricated, the headline drops to Unreliable"].

### Link status counts

| ACCESSIBLE | GATED | DEAD | MISMATCH | NOT FOUND |
|---|---|---|---|---|
| [n] | [n] | [n] | [n] | [n] |

### Claim verdict counts

| VERIFIED | PARTIALLY SUPPORTED | INFERENCE | MISATTRIBUTED | CONTRADICTED | FABRICATED | NO CITATION | unevaluated |
|---|---|---|---|---|---|---|---|
| [n] | [n] | [n] | [n] | [n] | [n] | [n] | [n] |

## Structural Integrity

- Inline citations: [N] | Reference entries: [N]
- Orphaned: [n] | Unused: [n] | Duplicates: [n]
```

## Systemic Warning

Print immediately under the grades whenever any claim is FABRICATED — assigned by you or confirmed by the user:

```markdown
> ⚠️ **Systemic warning — fabrication confirmed.** At least one citation in this
> document was invented ([claim IDs]). A model that hallucinated one source cannot
> be assumed honest about the rest. Treat every citation in this document —
> including the VERIFIED ones — with elevated skepticism, and independently
> spot-check any claim you intend to rely on.
```

## Critical Findings

Order sections by severity. Omit empty sections.

```markdown
## Critical Findings

### Fabricated claims

| ID | Claim | Citation | Evidence |
|---|---|---|---|
| C[n] | "[claim]" | [N] | Source [does not contain it / not found]; cross-verification search found nothing: [queries used] |

### Contradicted claims

| ID | Claim | Citation | Source actually says |
|---|---|---|---|
| C[n] | "[claim]" | [N] | "[opposing statement, paraphrased]" |

### Misattributed claims

| ID | Claim | Citation | Issue |
|---|---|---|---|
| C[n] | "[claim]" | [N] | Source says [actual]; [corroborated at (sources) / fabrication not checked — low stakes] |

### Uncited claims

| Location | Claim | Why it needs a citation |
|---|---|---|
| Section X, para 2 | "[statistic or quote]" | [quantitative claim / direct quote / external-entity claim] |

### Citation metadata errors

| Citation | Field | Cited as | Actually | Severity |
|---|---|---|---|---|
| [N] | [author/title/date/publication/URL] | [claimed value] | [real value] | [major/minor] |

### Source quality flags

| Citation | Characterization | Flag |
|---|---|---|
| [N] | [press release / blog / …] | [self-interested sourcing: claim about X backed by X's own material / provenance mismatch: framed as research, backed by self-published source] |

### Partially supported and inference claims

| ID | Verdict | Claim | Gap |
|---|---|---|---|
| C[n] | PARTIALLY SUPPORTED | "[claim]" | [scope/magnitude gap] |
| C[n] | INFERENCE | "[claim]" | [what the source states vs what was derived] |
```

## Manual Audit — NOT FOUND items

One section per NOT FOUND source. This is a handoff to the user: give them everything you did so they don't retrace your steps.

```markdown
## Manual Audit Required: [k] source(s) could not be located

### Pending item [1] — citation [N]: "[cited title]"

- **Cited URL**: [url]
- **Fetch result**: `[verbatim error, e.g. {"error_type": "ROBOTS_DISALLOWED", ...}]`
- **Searches run**: [queries, verbatim]
- **What came back**: [summary — nothing / unrelated results / similar-but-different source]
- **Claims affected**: C[n] ("[claim]"), C[m] ("[claim]")
- **Cross-verification**: [claim corroborated at (sources) → lower concern | claim found nowhere → HIGH CONCERN]

**Your call — reply with one per item:**
1. "Real, but I can't get you the content" → becomes GATED; claims stay unevaluated, disclosed
2. "Real — here's the content or a working link" → I evaluate the claims normally
3. "Confirmed fabricated" → FABRICATED penalty + systemic warning
4. "Still unknown" → stays pending, disclosed

I'll re-run the grades after your classifications.
```

## Quick Summary

```markdown
## Quick Summary

**Headline**: [tier] (worse of: link [tier], claims [tier])
**Checked**: [n] of [N] sources; [n] of [N] claims

**Action required:**
- [ ] Classify [k] pending NOT FOUND source(s) — see Manual Audit
- [ ] Review [n] misattributed/contradicted claim(s)
- [ ] Add citations for [n] uncited claim(s)

**Top issues:**
1. [Most severe finding, with claim ID]
2. [Second]
3. [Third]
```

## Full Audit Log

On request, or for documents small enough to log fully:

```markdown
## Full Audit Log

### Citation [1] — "[cited title]"
**Link status**: [tag] [(via archive / recovered from bad URL) if applicable]
**Metadata**: title [exact/paraphrased/wrong] · author [correct/wrong/missing] · date [correct/wrong] · publication [correct/wrong] · URL [correct/wrong-but-source-real]
**Source quality**: [type; independence/representation flags if any]

**Claims citing this source:**
1. **C[n]** — "[claim text]" (Section X)
   - **Verdict**: [tag]
   - **Evidence**: [what the source says, where; for composite claims, itemize which atomic facts held and which failed]

---
[Continue per citation…]
```

## Sample Output (abbreviated)

```markdown
# Citation Audit Report

**Document**: Consumer Attitudes on Sustainability
**Audit date**: 2026-07-18
**Sources**: 12 distinct (13 entries; 1 duplicate collapsed)
**Claims**: 21 claims under audit, IDs C1–C21 in document order (20 with citations, 1 uncited finding)

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

### Link status counts

| ACCESSIBLE | GATED | DEAD | MISMATCH | NOT FOUND |
|---|---|---|---|---|
| 9 | 1 | 1 | 0 | 1 |

### Claim verdict counts

| VERIFIED | PARTIALLY SUPPORTED | INFERENCE | MISATTRIBUTED | CONTRADICTED | FABRICATED | NO CITATION | unevaluated |
|---|---|---|---|---|---|---|---|
| 12 | 3 | 1 | 1 | 0 | 0 | 1 | 3 |

## Critical Findings

### Misattributed claims

| ID | Claim | Citation | Issue |
|---|---|---|---|
| C4 | "over 80% of respondents are concerned about environmental issues affecting them now" | [1] | Source says 80% concerned about *future* impact; corroborated nowhere for "now" framing — but claim is qualitative, fabrication not checked |

## Manual Audit Required: 1 source could not be located

### Pending item 1 — citation [9]: "Global Retail Sustainability Index 2025"

- **Cited URL**: https://www.grsi-institute.org/reports/2025-index
- **Fetch result**: `{"error_type": "ROBOTS_DISALLOWED", "error_message": "Site disallows automated access..."}`
- **Searches run**: "Global Retail Sustainability Index 2025", "GRSI Institute retail sustainability report"
- **What came back**: no organization or report by this name; no domain traces
- **Claims affected**: C15 ("retail emissions fell 12% among index leaders"), C16
- **Cross-verification**: C15 found nowhere → HIGH CONCERN
```
