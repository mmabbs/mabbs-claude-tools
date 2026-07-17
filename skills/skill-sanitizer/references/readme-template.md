# Public README Template

The README is human onboarding. The SKILL.md is Claude's instructions. Never conflate them: the README shows the skill *doing something* — it never paraphrases the frontmatter description.

## Structure

Use these sections in this order. Skip a section only when it genuinely doesn't apply.

1. **What it does** — one paragraph, then the workflow as a short numbered list.
2. **Sample output** — a concrete example of what the skill produces. Real-shaped content, not a template with placeholders.
3. **Requirements** — a table with three columns: component, required/optional, and "Without it" (what degrades). Document the graceful degradation that already exists — 10–15 lines total, never a separate configuration guide per permutation.
4. **Installation** — the clone-and-copy recipe. If the skill bundles agent files, include the step copying them to `~/.claude/agents/`.
5. **Configuration / Adapting** — only when the skill has regional identity or documented coupling. List exactly what to swap and where.
6. **Bundled files** — a table of what ships in the folder and what each file is for.
7. **Vault assumptions** — only for skills with integral vault coupling: frontmatter schema, folder structure, naming conventions the skill expects.

## Writing rules

- **Show, don't claim.** A sample output earns more trust than an adjective.
- **Name competitors directly when positioning.** No categorical claims ("only tool that...") unless verified. Add an "Honest expectations" note where results vary by setup.
- **Requirements tell the reader what they lose, not just what they need.** "Without Playwright: falls back to fetch, no JS-rendered pages" beats "Playwright recommended."
