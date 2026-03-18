#!/bin/bash
# Agent activation hook - enables /agent-name slash commands
# This hook intercepts slash commands and activates corresponding agents

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$PROJECT_ROOT/.claude-agents-config.json"
AGENTS_DIR="$PROJECT_ROOT"

# Load agent configuration
if [ ! -f "$CONFIG_FILE" ]; then
    echo "Error: Agent configuration not found at $CONFIG_FILE"
    exit 1
fi

# Parse the slash command from Claude Code
COMMAND="$1"

# Extract agent name from shortcuts or direct reference
AGENT_NAME=""

# Check if it's a shortcut
if jq -e ".shortcuts.\"$COMMAND\"" "$CONFIG_FILE" > /dev/null 2>&1; then
    AGENT_NAME=$(jq -r ".shortcuts.\"$COMMAND\"" "$CONFIG_FILE")
else
    # Assume direct agent name
    AGENT_NAME="${COMMAND#/}"
fi

# Find the agent file
AGENT_FILE=""
for category in academic design engineering marketing sales strategy testing product project-management support specialized game-development spatial-computing paid-media; do
    CANDIDATE="$AGENTS_DIR/$category/$AGENT_NAME.md"
    if [ -f "$CANDIDATE" ]; then
        AGENT_FILE="$CANDIDATE"
        break
    fi
done

if [ -z "$AGENT_FILE" ]; then
    echo "❌ Agent not found: $AGENT_NAME"
    echo "Available shortcuts: $(jq -r '.shortcuts | keys | join(", ")' "$CONFIG_FILE")"
    exit 1
fi

# Read and output the agent prompt
if [ -f "$AGENT_FILE" ]; then
    echo "✅ Activated: $AGENT_NAME"
    echo ""
    cat "$AGENT_FILE"
else
    echo "❌ Agent file not found: $AGENT_FILE"
    exit 1
fi
