#!/bin/bash
# Display subagent and skill calls on screen

if [ "$TOOL_NAME" = "Task" ]; then
    SUBAGENT_TYPE=$(echo "$TOOL_ARGS" | jq -r '.subagent_type // "unknown"')
    DESCRIPTION=$(echo "$TOOL_ARGS" | jq -r '.description // ""')
    echo "🤖 Subagent: $SUBAGENT_TYPE → $DESCRIPTION"

elif [ "$TOOL_NAME" = "Skill" ]; then
    SKILL_NAME=$(echo "$TOOL_ARGS" | jq -r '.skill // "unknown"')
    SKILL_ARGS=$(echo "$TOOL_ARGS" | jq -r '.args // ""')
    if [ -n "$SKILL_ARGS" ]; then
        echo "⚡ Skill: $SKILL_NAME ($SKILL_ARGS)"
    else
        echo "⚡ Skill: $SKILL_NAME"
    fi
fi
