# mabbs-claude-tools
A small collection of skills I use in my own Claude workflow, cleaned up so anyone can install them. Each is a self-contained folder you copy into a skills directory (one, `research-auditor-desktop`, uploads to claude.ai/Desktop as a ZIP instead). No marketplace, plugin, or build step.

New to Claude skills? Check out [Anthropic's docs on Claude Skills](https://code.claude.com/docs/en/skills)

## Skills

### Thinking

| Skill                    | What it does                                                                                                                                | Notes         |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------- | ------------- |
| [ideate](skills/ideate/) | 16 structured thinking modes (collision, inversion, first-principles, steelmanning, and more) for working a stuck problem from a new angle. | Requires Opus |

### Research

| Skill                                                        | What it does                                                                                                                                                                                  | Notes                                        |
| ------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------- |
| [research-auditor-desktop](skills/research-auditor-desktop/) | Audits citation integrity in research documents: verifies each cited source is real and reachable, checks whether sources say what the document claims, and grades on two axes (link integrity, claim accuracy). | claude.ai/Desktop upload · needs web access |

### Skill development

| Skill                                | What it does                                                                                                                                              | Notes                        |
| ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------- |
| [skill-critic](skills/skill-critic/) | Adversarial design review for your skills: a steelman argues against the design, a defender rates each criticism, a blind tester attempts a real task, and the synthesis proposes fixes. | Requires Opus · manual-only |
| [skill-sanitizer](skills/skill-sanitizer/) | Takes a personal skill and produces a copy ready for public release — strips personal data, applies portability fixes, writes the public README, gates the repo move with a final sweep. | manual-only |

### Claude Code setup

| Skill                                    | What it does                                                                                                                                                          | Notes                          |
| ---------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------ |
| [cc-health](skills/cc-health/)           | Plugin that audits Claude Code infrastructure across 7 domains (chats, config, assets, memory, version compat, debris, temp files) with Python scanners and a SessionStart hook. | Plugin install · Opus for version domain |
| [config-audit](skills/config-audit/)     | Audits every Claude Code config layer (rules, skills, hooks, plugins, MCP, memory, CLAUDE.md, agents) and recommends what to relocate, consolidate, or create.        | Spawns subagents · Opus recommended |

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
- **Plugin install** — `cc-health` is a plugin, not a standalone skill. It requires the local plugin install flow (`claude plugin marketplace add` + `claude plugin install`). See its README for the full steps.
- **Subagent-heavy** — `config-audit` spawns eight parallel scanner agents plus one reasoning agent per run. It targets Sonnet for scanning and Opus for the cross-layer reasoning; without those models it falls back to your session model.
- **Desktop upload** — `research-auditor-desktop` is for claude.ai / Claude Desktop, not Claude Code: don't copy it into `~/.claude/skills/`. Rename the folder to `research-auditor` and upload it as a ZIP via Settings → Capabilities → Skills — its README has the exact packaging steps.
- **Model requirements** — `ideate` requires Opus. Its frameworks are reasoning-intensive; lower-tier models produce shallow output that defeats the purpose. Solo modes technically function on Sonnet but with degraded quality; combinations and agent pipelines are not recommended without Opus.

## Maintenance and contributions

These are tools I build and maintain for my own use. I make a genuine effort to review issues and pull requests, but I can't promise a response time or that I'll merge. Treat it as best-effort, not a supported product. Fork freely.
