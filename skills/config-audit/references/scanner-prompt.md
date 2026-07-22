# Scanner Prompt Template

Fill in `[TYPE]`, the paths from the "What Each Scanner Reads" table in SKILL.md, and the resolved `<workspace>` path, then pass to each scanner agent. Include any scanner-specific instructions from the table row (e.g., the hooks scanner's plugin enabled-state check).

---

Scan [TYPE] configuration at the paths listed below. For each item, record five fields:

1. **Name** — filename or identifier
2. **Path** — full path
3. **Purpose** — what it does, one line
4. **Cross-references** — mentions of other config types (a rule referencing a memory file, a hook calling a skill, a CLAUDE.md section duplicating a rule, etc.). "None" if clean.
5. **Content character** — classify what kind of content this is:
   - **Behavioral**: prescribes how Claude should act ("always do X", "when X, do Y")
   - **Context**: describes the project, user, or environment for Claude's understanding
   - **Pointer**: directs Claude to an external resource ("read this file", "check this URL")
   - **Procedural**: step-by-step workflow instructions ("first do X, then Y")
   - **Enforcement**: blocks or allows actions based on conditions ("reject if X", "only permit Y")

Write the inventory to: `<workspace>/inventory-<type>.md`

Do not assess whether items are misplaced. Do not recommend changes. Catalog accurately.
Note dead-weight items (empty files, no-op scripts, orphaned caches) in the inventory but tag them as `[dead-weight]` — config-audit does not act on these. Dead-weight cleanup is a separate maintenance concern, outside this skill's scope.

Use this inventory format:

```markdown
# Inventory: [Config Type]

Scanned: [date]
Paths checked: [list]

## Items

### [item-name]
- **Path:** /full/path
- **Purpose:** one line
- **Cross-references:** [list, or "none"]
- **Content character:** behavioral | context | pointer | procedural | enforcement

[repeat for each item]

## Summary
- Total items: N
- Cross-layer references: [list which items reference what]
- Content character breakdown: N behavioral, N context, N pointer, N procedural, N enforcement
```
