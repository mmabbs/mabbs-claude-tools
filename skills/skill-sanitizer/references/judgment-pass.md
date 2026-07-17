# Judgment Pass

These are keep/remove calls where past sanitization runs needed the user's correction. Present all findings in one message — for each: the finding, a recommendation, and the reasoning. Apply only after the user decides. Non-interactive runs apply the recommendation and mark it `AUTO-APPLIED`.

## 1. Core identity vs. author-interest layer

- **Test each domain-specific element: does removing it change what the skill IS, or just who it's tuned for?** Regional or topical identity (a Toronto events skill, a Canadian AI news skill) is the skill's identity — keep it and add an "Adapting" section to the README. A personal interest layered on top (a game-dev category inside a general events skill) narrows the audience — recommend removing it.

## 2. Personal-constraint rules

- **Remove rules that encode the author's private situation.** "Exclude Mississauga events" existed because the author couldn't easily get there — invisible context an adopter can't reason about. If the rule's reason lives outside the skill, recommend removal.

## 3. Coupling: document or abstract

- **When personal data wraps generic logic, abstract the data and keep the mechanism.** Swap real values for examples headed "Example — replace with your own." The logic stays untouched.
- **When coupling is integral, document it instead.** If abstracting the vault assumptions would gut the skill's value, keep them and write a prominent "Vault Assumptions" section in the README: frontmatter schema, folder structure, naming conventions.

## 4. Positioning claims

- **Cut categorical market claims the research can't carry.** "Fills a gap no product fills" becomes naming the actual competitors and what each does. Add honest-expectations framing where results vary.
- **Frame overlap with built-in features as complementary halves, not competition.** "Discovery half / action half" beats "we still do something useful."

## 5. Proactive triggers

- **Remove out-of-invocation proactive behavior** ("ALWAYS suggest this when the session is wrapping up") — it competes with unknown setups in adopters' environments. Functional `argument-hint` values are passive autocomplete, not proactive triggers — those stay.

## 6. Model requirements

- **Keep hard model requirements hard.** State the requirement prominently with its reasoning inlined. Do not soften to "use X if available" — a soft fallback silently degrades the skill for users who don't know why the model matters.

## 7. Structure

- **Merge platform variants into one SKILL.md with a mode table when content overlap exceeds ~80%.** Separate variant files are justified only when the core execution strategy differs fundamentally.
- **Reorganize flat folders past ~5–6 root files.** Implementation files move into `scripts/`, `references/`, or purpose-named subfolders; SKILL.md and README stay at root. Update every internal reference after moving.

## 8. Working documents

- **Fold working docs (positioning notes, planning files) into the README, then delete them.** They were scaffolding, not product.
