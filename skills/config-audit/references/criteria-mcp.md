# Criteria: MCP Servers

What makes something an MCP server (`.mcp.json`, `claude mcp add`, or plugin-bundled) rather than a CLI tool called via Bash, a skill with scripts, or a plugin question.

## What Earns Its Keep

An MCP server earns its keep when it provides at least one of four mechanical benefits:

1. **Live external integration.** A persistent, bidirectional connection to a running service: typed tools, resources addressable by `@mention` (`github:issue://123`), prompt templates surfaced as slash commands, mid-task user input requests (elicitation), dynamic tool-list updates, and automatic reconnection. Nothing else in the config system *connects* to anything — every other type is files read at load time.
2. **Authentication handling.** OAuth 2.0 flows (dynamic client registration, metadata discovery, scope pinning), header helpers for custom auth schemes, tokens stored in the system keychain. The alternative — API keys pasted into scripts or env vars for Bash calls — is both less secure and manual to maintain.
3. **Typed tool surface.** Each tool has a schema the model fills, a stable name (`mcp__server__tool`) that permission rules and hook matchers target precisely, and per-tool approval semantics. A Bash-invoked CLI is one opaque `Bash` permission; an MCP server's tools are individually governable.
4. **Deferred schema loading.** Tool search loads only names and server instructions at startup, fetching full schemas on demand — so a large tool surface scales without a proportional context tax.

**The test:** does the integration need auth, persistent connection or session state, or a governable per-tool permission surface? Those are the three things Bash and scripts genuinely can't provide.

## What Disqualifies

1. **A CLI already does the job.** `gh`, `git`, `jq`, `curl` — a tool Claude can call via Bash costs zero standing context and needs no server process. Wrapping a working CLI in MCP adds schema overhead and a daemon to babysit for no new capability.
2. **Static data.** Information that doesn't change mid-session belongs in a file Claude reads on demand — a reference doc, a skill's supporting file. A server whose tools return constants is a document with a process attached.
3. **No external system.** If the logic is pure prompting or local file manipulation, it's a skill (with scripts if it needs code). MCP's machinery exists to bridge to *other systems*.
4. **One-off fetches.** A URL Claude needs once is WebFetch or `curl`, not an integration.
5. **Prompt templates as the payload.** MCP prompts technically surface as slash commands, but skills are the native mechanism — richer frontmatter, supporting files, no server required. An MCP server justified mainly by its prompts is a skills directory in disguise.

## Boundary Cases

### MCP Server vs. CLI via Bash

The most common call. Default to the CLI; escalate to MCP when you hit one of the three walls: (a) auth the CLI can't hold securely, (b) state or a connection that must persist across calls, (c) the need to allow some operations but not others at permission level. GitHub illustrates both sides: `gh` covers most workflows via Bash, while the GitHub MCP server earns its place when OAuth scoping and per-tool permissioning matter.

### MCP Server vs. Skill with Scripts

A skill's scripts execute locally, on demand, inside the skill's procedure — right for computation, transformation, and local automation. MCP is right when the counterpart is a *service*: something that authenticates, holds state, or pushes updates. Litmus: if the script would have to manage its own tokens and re-implement retry/reconnect logic, that's MCP's job description.

### MCP Server vs. Plugin

Orthogonal — an MCP server is a component a plugin can carry, not a competing type. Personal integration → `claude mcp add` (user scope for cross-project tools, project scope in `.mcp.json` for team-shared). Distributing the server, or shipping it with companion skills and hooks → plugin packaging, with the tool-name consequence that matchers and permissions must use the longer `mcp__plugin_<plugin>_<server>__<tool>` form.

### MCP Server vs. Hook

Hooks can use MCP: an `mcp_tool`-type hook calls a tool on a connected server when an event fires. So "I want the linter service pinged on every edit" isn't a choice between the two — the MCP server provides the capability; the hook provides the trigger.

## Context Cost Discipline

Even with tool search deferring schemas, every connected server contributes names and instructions to startup context, and every enabled server is a process (or connection) plus a permission surface. Audit periodically: a server whose tools haven't been called in weeks is paying rent for nothing — disconnect it and fall back to CLI or on-demand fetches until it's needed again. Scope deliberately when adding: `--scope project` for project-specific servers, `--scope user` only for genuinely cross-project tools.
