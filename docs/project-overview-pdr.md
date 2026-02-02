# Project Overview & Product Development Requirements

## Overview

This repository contains Claude Code Skills, Agents, and Workflows - modular packages that extend Claude's capabilities with specialized knowledge, workflows, and tool integrations.

## Repository Structure

| Directory | Purpose |
|-----------|---------|
| `agents/` | Subagent definitions for orchestration |
| `skills/` | Skill packages (SKILL.md + scripts/references/assets) |
| `workflows/` | Development guidelines and orchestration protocols |
| `docs/` | Project documentation and standards |
| `plans/` | Implementation plans (created during development) |

## Core Components

### Agents (17 total)
Specialized subagents for different tasks:
- **Orchestration**: implementer, project-manager
- **Planning**: brainstormer, planner, researcher
- **Quality**: code-reviewer, tester, debugger
- **Documentation**: docs-manager
- **Specialized**: ui-ux-designer, database-admin, git-manager, scout, mcp-manager, copywriter, journal-writer

### Skills
Modular capability packages containing:
- `SKILL.md` (required) - Instructions with YAML frontmatter
- `scripts/` (optional) - Executable code
- `references/` (optional) - Documentation for context
- `assets/` (optional) - Templates, images, fonts

### Workflows
Development protocols:
- `primary-workflow.md` - Main development process
- `orchestration-protocol.md` - Agent chaining patterns
- `development-rules.md` - Coding standards
- `documentation-management.md` - Doc update triggers

## Product Requirements

### Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-01 | Skills must be self-contained with SKILL.md under 100 lines | High |
| FR-02 | Agents must define clear delegation patterns | High |
| FR-03 | Workflows must support sequential and parallel execution | High |
| FR-04 | Plans must be stored in `./plans/` with standardized structure | Medium |
| FR-05 | Reports must follow naming convention for handoffs | Medium |

### Non-Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| NFR-01 | Token efficiency - minimize context usage | High |
| NFR-02 | Cross-platform compatibility (Node.js/Python preferred over bash) | High |
| NFR-03 | Progressive disclosure - split large docs into references | Medium |
| NFR-04 | Consistent formatting across all documentation | Medium |

### Constraints

- SKILL.md files must be under 100 lines
- Referenced markdown files also under 100 lines
- Scripts must include tests
- Environment variables: `process.env` > skill `.env` > parent `.env`

## Success Metrics

| Metric | Target |
|--------|--------|
| Skill self-containment | 100% of skills work standalone |
| Agent clarity | Each agent has single responsibility |
| Documentation coverage | All public APIs documented |
| Test coverage | Scripts include test cases |

## Dependencies

- Claude Code CLI
- Node.js or Python (for scripts)
- Git (for version control)

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-02-02 | Initial documentation structure |
