#!/bin/bash
# Detect Claude Code version changes and nudge the user.
# Reads $CLAUDE_CODE_EXECPATH (set by CC runtime). No subprocess calls.
# Known limitation: change detection compares the execpath basename as an
# opaque string, not a parsed semver. On installs where the basename is a
# constant binary name (not a version), no nudge ever fires.

current=$(basename "$CLAUDE_CODE_EXECPATH" 2>/dev/null)
plugin_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# State lives outside the plugin tree so upgrades don't wipe it
state_file="$HOME/.claude/cc-health-state.json"
legacy_state="$plugin_root/state/.cc-health-state.json"

# No execpath → not running under Claude Code (testing, cron, etc.)
if [[ -z "$current" ]]; then exit 0; fi

# One-time migration from the pre-2.0.1 in-plugin location
if [[ ! -f "$state_file" && -f "$legacy_state" ]]; then
  cp "$legacy_state" "$state_file" 2>/dev/null
fi

mkdir -p "$HOME/.claude"

# First run → initialize state, no nudge
if [[ ! -f "$state_file" ]]; then
  printf '{"lastSeenVersion":"%s","lastAuditTimestamp":null,"domainRuns":{}}\n' "$current" > "$state_file"
  exit 0
fi

# Read last-seen version (python3 is at /usr/bin/python3 — safe in stripped PATH)
last=$(/usr/bin/python3 -c "import json,sys; print(json.load(open('$state_file')).get('lastSeenVersion',''))" 2>/dev/null)

if [[ "$current" != "$last" && -n "$last" ]]; then
  echo "CC updated $last → $current — run /cc-health version to check for breaking changes."
fi
