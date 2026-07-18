#!/bin/bash
# Detect Claude Code version changes and nudge the user.
# Reads $CLAUDE_CODE_EXECPATH (set by CC runtime). No subprocess calls.

current=$(basename "$CLAUDE_CODE_EXECPATH" 2>/dev/null)
plugin_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
state_file="$plugin_root/state/.cc-health-state.json"

# No execpath → not running under Claude Code (testing, cron, etc.)
if [[ -z "$current" ]]; then exit 0; fi

# Ensure state directory exists
mkdir -p "$plugin_root/state"

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
