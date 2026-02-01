---
name: mcp-management
description: Manage Model Context Protocol (MCP) servers - discover, analyze, and execute tools/prompts/resources from configured MCP servers. Use when working with MCP integrations, need to discover available MCP capabilities, filter MCP tools for specific tasks, execute MCP tools programmatically, access MCP prompts/resources, or implement MCP client functionality. Supports intelligent tool selection, multi-server management, and context-efficient capability discovery.
---

# MCP Management

Manage and interact with Model Context Protocol (MCP) servers.

## Overview

MCP enables AI agents to connect to external tools and data sources. This skill provides context-efficient discovery and execution of MCP capabilities.

## Quick Start

**Method 1: Gemini CLI (recommended)**
```bash
npm install -g gemini-cli
mkdir -p .gemini && ln -sf .claude/.mcp.json .gemini/settings.json
echo "Take a screenshot of https://example.com. Return JSON only." | gemini -y -m gemini-2.5-flash
```

**Method 2: Direct Scripts**
```bash
cd .claude/skills/mcp-management/scripts && npm install
npx tsx cli.ts list-tools       # Saves to assets/tools.json
npx tsx cli.ts call-tool memory create_entities '{"entities":[...]}'
```

## Execution Priority

1. **Gemini CLI** (Primary): `echo "<task>" | gemini -y -m gemini-2.5-flash`
2. **Direct CLI Scripts**: `npx tsx scripts/cli.ts call-tool <server> <tool> <args>`
3. **mcp-manager Subagent** (Fallback): Context-efficient delegation

## CLI Commands

```bash
npx tsx scripts/cli.ts list-tools      # Display all tools, save to assets/tools.json
npx tsx scripts/cli.ts list-prompts    # Display all prompts
npx tsx scripts/cli.ts list-resources  # Display all resources
npx tsx scripts/cli.ts call-tool <server> <tool> <json>  # Execute tool
```

## Configuration

MCP servers configured in `.claude/.mcp.json`. For Gemini CLI:
```bash
mkdir -p .gemini && ln -sf .claude/.mcp.json .gemini/settings.json
```

## Reference Documentation

| Document | Description |
|----------|-------------|
| [configuration.md](references/configuration.md) | Config file setup, server definitions |
| [gemini-cli-integration.md](references/gemini-cli-integration.md) | Gemini CLI usage, GEMINI.md format |
| [mcp-protocol.md](references/mcp-protocol.md) | JSON-RPC details, transport, error codes |

## Key Benefits

- Progressive disclosure (load only what's needed)
- Multi-server management from single config
- Persistent tool catalog in `assets/tools.json`
- Context-efficient: subagents handle MCP operations
