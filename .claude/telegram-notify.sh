#!/bin/bash
# Telegram notification hook for Claude Code
# Sends a message when Claude finishes a task.
#
# Setup:
#   1. Copy this file to ~/.claude/telegram-notify.sh
#   2. Fill in TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID below
#   3. chmod +x ~/.claude/telegram-notify.sh
#   4. Add to ~/.claude/settings.json Stop hooks:
#      { "type": "command", "command": "~/.claude/telegram-notify.sh" }

TELEGRAM_BOT_TOKEN="${TELEGRAM_BOT_TOKEN:-}"
TELEGRAM_CHAT_ID="${TELEGRAM_CHAT_ID:-}"

if [[ -z "$TELEGRAM_BOT_TOKEN" || -z "$TELEGRAM_CHAT_ID" ]]; then
  exit 0
fi

# Read JSON input from stdin
input=$(cat)

# Recursion prevention
stop_hook_active=$(echo "$input" | jq -r '.stop_hook_active // false')
if [[ "$stop_hook_active" = "true" ]]; then
  exit 0
fi

# Get project name from cwd
cwd=$(echo "$input" | jq -r '.cwd // ""')
project=$(basename "$cwd")

# Build message
if [[ -n "$project" ]]; then
  message="✅ Claude Code 任务完成了！
📁 项目：$project"
else
  message="✅ Claude Code 任务完成了！"
fi

# Send Telegram notification
curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
  -H "Content-Type: application/json" \
  -d "{\"chat_id\": \"${TELEGRAM_CHAT_ID}\", \"text\": \"${message}\"}" \
  > /dev/null 2>&1

exit 0
