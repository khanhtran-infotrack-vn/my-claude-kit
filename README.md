# Claude Code Skills, Agents & Workflows

Modular packages that extend Claude Code with specialized knowledge, workflows, and tool integrations.

## Quick Start

```bash
# Use a skill
/skill-name

# Trigger implementer for full feature delivery
"Implement [feature]" or "Let's cook [feature]"

# Brainstorm before implementing
"Should we use X or Y?" → brainstormer explores options
```

## Structure

```
├── agents/      # 17 subagents for orchestration
├── skills/      # Capability packages (SKILL.md + scripts/references/assets)
├── workflows/   # Development protocols
├── docs/        # Project documentation
└── plans/       # Implementation plans (created during development)
```

## Primary Workflow

```
                    ┌──────────────┐
                    │ brainstormer │ (optional - for unclear requirements)
                    └──────┬───────┘
                           ▼
┌──────────────────────────────────────────────────────────────────────┐
│                    implementer (orchestrates)                         │
│  ┌─────────┐   ┌─────────┐   ┌────────┐   ┌─────────────┐           │
│  │ planner │ → │  code   │ → │ tester │ → │code-reviewer│           │
│  └─────────┘   └─────────┘   └────────┘   └─────────────┘           │
│                                                   ↓                  │
│                              ┌─────────────────┬─────────────┐      │
│                              │ project-manager │ docs-manager│      │
│                              └─────────────────┴─────────────┘      │
└──────────────────────────────────────────────────────────────────────┘
```

## Agents

| Agent | Purpose |
|-------|---------|
| **brainstormer** | Explore options, debate trade-offs (advisory only) |
| **planner** | Create implementation plans in `./plans/` |
| **implementer** | End-to-end feature delivery orchestrator |
| **code-reviewer** | Quality, security, performance review |
| **tester** | Test execution and validation |
| **debugger** | Issue investigation and diagnosis |
| **project-manager** | Progress tracking, roadmap updates |
| **docs-manager** | Documentation maintenance |
| **researcher** | Technical research |
| **scout** | Codebase file search |
| **ui-ux-designer** | Frontend design |
| **git-manager** | Commit operations |
| **database-admin** | Database operations |

[Full agent details →](agents/README.md)

## Skills

Each skill contains:
- `SKILL.md` (required) - Instructions (<100 lines)
- `scripts/` (optional) - Executable code with tests
- `references/` (optional) - Documentation chunks
- `assets/` (optional) - Templates, images

```bash
# Initialize new skill
scripts/init_skill.py <skill-name> --path <output-directory>

# Package for distribution
scripts/package_skill.py <path/to/skill-folder>
```

## Documentation

| Document | Description |
|----------|-------------|
| [Project Overview & PDR](docs/project-overview-pdr.md) | Requirements, constraints, success metrics |
| [Project Roadmap](docs/project-roadmap.md) | Phases, milestones, changelog |
| [Code Standards](docs/code-standards.md) | Conventions, naming, quality gates |
| [System Architecture](docs/system-architecture.md) | Component diagrams, data flow |

## Core Principles

- **YAGNI** - Don't add functionality until necessary
- **KISS** - Prefer simple solutions
- **DRY** - Extract common patterns
- **SOLID** - For .NET/C# projects

## Key Constraints

- SKILL.md must be under 100 lines
- Referenced markdown files also under 100 lines
- Scripts must include tests
- Prefer Node.js/Python over bash for cross-platform compatibility
- Token efficiency - minimize context usage
