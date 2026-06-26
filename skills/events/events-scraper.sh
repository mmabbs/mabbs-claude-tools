#!/bin/bash
# Toronto Events Scraper — Claude Code headless cron script
# Schedule: daily at 8AM (or your preferred time)
#   crontab: 0 8 * * 1-5 /path/to/events-scraper.sh
#
# Configure the two variables below before first run.

# --- USER CONFIGURATION ---
VAULT="$HOME/path/to/your/vault"
OUTPUT_DIR="$VAULT/path/to/your/events-folder"  # where event notes and source-health.json are written
CITY="toronto"                                   # used in filenames: <city>-events-YYYY-MM-DD.md
CLAUDE_BIN="$HOME/.local/bin/claude"             # adjust to your claude binary path
MODEL="claude-sonnet-4-6"                        # update when models are renamed/retired
                                                  # check available models: claude model list
# --------------------------

# Log directory — override with EVENTS_LOG_DIR; default works on Linux and macOS.
LOG_DIR="${EVENTS_LOG_DIR:-$HOME/.local/state/events-scraper}"
mkdir -p "$LOG_DIR"

[ -x "$CLAUDE_BIN" ] || { echo "Error: claude binary not found at $CLAUDE_BIN" >&2; exit 1; }
[ -d "$VAULT" ] || { echo "Error: vault directory not found at $VAULT" >&2; exit 1; }
[ -d "$OUTPUT_DIR" ] || { echo "Error: output directory not found at $OUTPUT_DIR" >&2; exit 1; }

cd "$VAULT" || exit 1
TODAY=$(date +%Y-%m-%d)
NOTE_FILE="$OUTPUT_DIR/${CITY}-events-$TODAY.md"

# Skip if today's note already exists
if [ -f "$NOTE_FILE" ]; then
    echo "$(date): Note already exists, skipping." >> "$LOG_DIR/events-scraper.log"
    exit 0
fi

# Ensure output directory exists
mkdir -p "$OUTPUT_DIR"

# Prevent collision with any active interactive session
unset CLAUDECODE

# Run Claude Code in headless mode
# Playwright tool IDs below use plugin-format names (claude plugin install playwright).
# If you installed Playwright MCP differently, find your tool IDs with:
#   claude mcp list | grep playwright
# and update the names below. Without matching IDs, Playwright is unavailable
# and scrapers fall back to WebFetch/Jina.
"$CLAUDE_BIN" -p "/events" \
    --model "$MODEL" \
    --allowedTools "Read,Write,Edit,WebFetch,Agent,Bash,Grep,Glob,ToolSearch,mcp__plugin_playwright_playwright__browser_navigate,mcp__plugin_playwright_playwright__browser_snapshot,mcp__plugin_playwright_playwright__browser_wait_for,mcp__plugin_playwright_playwright__browser_close" \
    --max-turns 35 \
    --no-session-persistence \
    >> "$LOG_DIR/events-scraper.log" 2>&1

echo "$(date): Run complete." >> "$LOG_DIR/events-scraper.log"
