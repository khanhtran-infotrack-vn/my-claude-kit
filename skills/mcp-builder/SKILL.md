---
name: mcp-builder
description: Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. Use when building MCP servers to integrate external APIs or services, whether in Python (FastMCP) or Node/TypeScript (MCP SDK).
---

# MCP Server Development Guide

Create high-quality MCP servers that enable LLMs to interact with external services.

## Development Workflow

### Phase 1: Research & Planning
1. Fetch MCP protocol: `https://modelcontextprotocol.io/llms-full.txt`
2. Read `reference/mcp_best_practices.md` for core guidelines
3. Study target API documentation exhaustively
4. Create implementation plan (tool selection, utilities, error handling)

### Phase 2: Implementation
1. Set up project structure
2. Implement core utilities (API helpers, pagination, error handling)
3. Implement tools systematically with proper schemas
4. Follow language-specific guides

### Phase 3: Review & Refine
1. Code quality review (YAGNI, KISS, DRY, SOLID)
2. Test and build
3. Use quality checklist

### Phase 4: Evaluations
1. Create 10 complex, realistic evaluation questions
2. Output as XML with question/answer pairs
3. See `reference/evaluation.md` for details

## Agent-Centric Design Principles

- **Workflows over endpoints** - Build task-oriented tools, not API wrappers
- **Optimize for context** - Return high-signal info, use concise formats
- **Actionable errors** - Guide agents toward correct usage
- **Natural task names** - Reflect how humans think about tasks

## Language Guides

**Python**:
- SDK: `https://github.com/modelcontextprotocol/python-sdk`
- Guide: `reference/python_mcp_server.md`
- Use Pydantic v2, async/await, type hints

**TypeScript**:
- SDK: `https://github.com/modelcontextprotocol/typescript-sdk`
- Guide: `reference/node_mcp_server.md`
- Use Zod schemas, strict mode, explicit types

## Tool Implementation Checklist

- [ ] Input schema with validation (Pydantic/Zod)
- [ ] Comprehensive docstrings with examples
- [ ] Error handling for all external calls
- [ ] Response format options (JSON/Markdown, concise/detailed)
- [ ] Character limits and truncation
- [ ] Tool annotations (readOnlyHint, destructiveHint, idempotentHint)

## Testing Notes

MCP servers are long-running. Don't run directly in main process.
- Use evaluation harness (recommended)
- Run in tmux
- Use timeout: `timeout 5s python server.py`

## Reference Documentation

- `reference/mcp_best_practices.md` - Universal guidelines
- `reference/python_mcp_server.md` - Python/FastMCP guide
- `reference/node_mcp_server.md` - TypeScript guide
- `reference/evaluation.md` - Evaluation creation
