# Criteria: Plugins

What makes something a plugin (`~/.claude/plugins/`, installed via marketplace or `claude plugin install`) rather than loose config files sitting in `skills/`, `agents/`, and settings.

## What Earns Its Keep

A plugin earns its keep when it provides at least one of five mechanical benefits:

1. **Bundling.** One plugin can package skills, agents, hooks, MCP servers, LSP servers, output styles, executables (`bin/` added to PATH), and default settings — components that serve one workflow ship and activate as a unit instead of being scattered across four directories and a settings file.
2. **Single toggle.** Enable/disable flips the whole capability set at once — hooks stop firing, skills leave the listing, MCP servers disconnect. Loose config has no off switch short of moving files.
3. **Distribution and versioning.** Marketplace installs, version pinning via `plugin.json`, auto-updates, dependency declarations. The only mechanism for sharing a multi-component capability with another person — or another machine — without copy-paste drift.
4. **Namespacing.** Components run as `plugin-name:component` (`/my-plugin:review`, agents as `my-plugin:reviewer`, MCP tools as `mcp__plugin_<plugin>_<server>__<tool>`), so a plugin never collides with local skills or other plugins.
5. **Lifecycle variables and user config.** `${CLAUDE_PLUGIN_ROOT}` (install dir), `${CLAUDE_PLUGIN_DATA}` (state that survives updates), and `userConfig` prompts at enable-time give plugin components portability and persistence that hardcoded paths in loose config can't match.

**The test:** multiple components serving one workflow, or any need to share, version, or cleanly toggle the capability. A single skill used on one machine earns none of this.

## What Disqualifies

1. **Single component, single machine, no sharing.** A loose skill or hook is simpler to create, edit, and debug. Plugin packaging adds a manifest, namespace, and install-state machinery for zero benefit.
2. **Rules or permissions as the payload.** Plugins cannot ship `.claude/rules/` files or permission entries — those stay user/project config. A "conventions plugin" whose content is behavioral rules has no mechanism to deliver them; it would have to fake it with hooks or skill descriptions.
3. **Heavy iteration expected.** An installed plugin updates through version churn (or reinstalls); a loose skill updates with one file edit. Develop as loose config first; package when it stabilizes. (Middle ground: a plugin developed in place under `skills/` with its own `.claude-plugin/plugin.json` loads as `<name>@skills-dir` — editable *and* packaged.)
4. **The components don't actually cohere.** A grab-bag plugin ("my stuff") bundles things with unrelated lifecycles, so the single toggle becomes a liability — you can't disable the noisy hook without losing the unrelated skills. Bundle by workflow, not by ownership.
5. **Settings as the main payload.** Plugin `settings.json` currently supports only two keys (`agent`, `subagentStatusLine`); everything else is silently ignored. A plugin that exists to configure Claude Code mostly can't.

## Boundary Cases

### Plugin vs. Loose Config

Count components and count consumers. One component × one machine → loose. Multiple components serving one workflow → plugin, even single-machine, for the toggle and the namespace. Anything shared beyond your machine → plugin, full stop; there is no other distribution mechanism.

### Plugin vs. Skill with Supporting Files

A skill directory already holds references, templates, and scripts — that covers most "skill plus helpers" cases without packaging. The line is crossed when the workflow needs components with *different activation mechanics*: a hook that must fire on events, an agent, an MCP server. Skills' supporting files can't do any of those; a plugin bundles all of them.

### Plugin vs. MCP Server

Not alternatives — an MCP server is a component a plugin can carry. The real question is packaging: an MCP server for yourself is a `claude mcp add` entry (user or project scope); an MCP server you're distributing, or one that ships with companion skills and hooks, rides inside a plugin. See criteria-mcp.md for when an MCP server is warranted at all.

### Plugin vs. Project `.claude/` Directory

A project's own `.claude/` (rules, skills, settings, committed to the repo) already distributes config to everyone who clones the project. Plugins are for capabilities that cross project boundaries. If it only ever applies to one repo, the repo's `.claude/` is the simpler home — and it can carry rules, which plugins can't.

## Install-State Discipline

Enabled and installed are separate, unvalidated systems: `enabledPlugins` in settings toggles a plugin; the install record pins where it lives, per scope (`user`/`project`/`local`). A plugin enabled globally but installed at project scope fails everywhere else with a misleading "not cached" error — and the `/plugin` TUI can only install at current-project scope. When a plugin misbehaves, check install-record scope against enable scope first (CLI repair: `claude plugin install <plugin>@<marketplace> --scope user`), and diagnose loading with `claude --debug`, not the error text.
