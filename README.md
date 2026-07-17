# mabbs-claude-tools
A small collection of skills I use in my own Claude Code workflow, cleaned up so anyone can install them. Each is a self-contained folder you copy into a skills directory. No marketplace, plugin, or build step.

New to Claude skills? Check out [Anthropic's docs on Claude Skills](https://code.claude.com/docs/en/skills)

## Skills

### Thinking

| Skill                    | What it does                                                                                                                                | Notes         |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------- | ------------- |
| [ideate](skills/ideate/) | 16 structured thinking modes (collision, inversion, first-principles, steelmanning, and more) for working a stuck problem from a new angle. | Requires Opus |

### Skill development

| Skill                                | What it does                                                                                                                                              | Notes                        |
| ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------- |
| [skill-critic](skills/skill-critic/) | Adversarial design review for your skills: a steelman argues against the design, a defender rates each criticism, a blind tester attempts a real task, and the synthesis proposes fixes. | Requires Opus · manual-only |
| [skill-sanitizer](skills/skill-sanitizer/) | Takes a personal skill and produces a copy ready for public release — strips personal data, applies portability fixes, writes the public README, gates the repo move with a final sweep. | manual-only |

### Local scene & monitoring

| Skill                      | What it does                                                                                       | Notes                                            |
| -------------------------- | -------------------------------------------------------------------------------------------------- | ------------------------------------------------ |
| [ai-news](skills/ai-news/) | Generates a Canadian AI-industry news digest covering funding, jobs, regulation, and market moves. | Region-configurable                              |
| [events](skills/events/)   | Scrapes local tech and AI events from several sources into one date-stamped, categorized note.     | Region-configurable · manual-only · writes files |

**Notes legend:** _manual-only_ — runs only when you invoke it, won't auto-trigger (set on skills that delete or write files); _region-configurable_ — ships with Canadian defaults you can repoint.

## Install

Each skill is one folder. Clone the repo and copy the folder you want into your skills directory:

```bash
git clone --depth 1 https://github.com/<user>/<repo>.git
cp -r <repo>/skills/ideate ~/.claude/skills/
```

- `~/.claude/skills/` installs a skill for every project. A project's own `.claude/skills/` scopes it to that repo.
- Claude Code detects newly added skills without a restart.
- Want one skill without cloning the whole repo? Use GitHub's "download folder" option, or [`degit`](https://github.com/Rich-Harris/degit) (requires Node 20+):

  ```bash
  degit <user>/<repo>/skills/ideate ~/.claude/skills/ideate
  ```

Replace `<user>/<repo>` with this repository's path.

## Before you run them

Some skills assume a particular environment. Each skill's own `README.md` documents its requirements, configuration, and how it behaves without them — the short version:

- **Obsidian-coupled** — `events` and `ai-news` write notes into an Obsidian vault. The per-skill READMEs list what to change for your own vault, or how to run them standalone.
- **Region-configurable** — `ai-news` and `events` default to Canadian and Toronto sources. Both document how to point them elsewhere.
- **Bundled scripts** — `events` includes a cron wrapper shell script that expects `claude` on your PATH.
- **Bundled agents** — `skill-critic` ships three agent definition files that must be copied to `~/.claude/agents/` (its README shows the exact step). They pin `claude-opus-4-6` deliberately — bump the pin on purpose, not via the auto-upgrading `opus` alias.
- **Model requirements** — `ideate` requires Opus. Its frameworks are reasoning-intensive; lower-tier models produce shallow output that defeats the purpose. Solo modes technically function on Sonnet but with degraded quality; combinations and agent pipelines are not recommended without Opus.

## Maintenance and contributions

These are tools I build and maintain for my own use. I make a genuine effort to review issues and pull requests, but I can't promise a response time or that I'll merge. Treat it as best-effort, not a supported product. Fork freely.
