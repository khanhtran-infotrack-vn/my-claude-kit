# System Architecture

## Overview

This system provides extensible AI agent orchestration through three core components: Skills, Agents, and Workflows.

```
┌─────────────────────────────────────────────────────────────────┐
│                        Claude Code CLI                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │   Skills    │  │   Agents    │  │  Workflows  │            │
│  │             │  │             │  │             │            │
│  │ Specialized │  │ Subagent    │  │ Orchestrate │            │
│  │ capabilities│  │ definitions │  │ patterns    │            │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
│         │                │                │                    │
│         └────────────────┼────────────────┘                    │
│                          ▼                                     │
│                 ┌─────────────────┐                           │
│                 │  Task Execution │                           │
│                 └─────────────────┘                           │
│                          │                                     │
│         ┌────────────────┼────────────────┐                   │
│         ▼                ▼                ▼                   │
│  ┌───────────┐   ┌───────────┐   ┌───────────┐              │
│  │  ./plans  │   │  ./docs   │   │  reports  │              │
│  └───────────┘   └───────────┘   └───────────┘              │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

## Component Architecture

### Skills Layer

Skills are self-contained capability modules.

```
┌─────────────────────────────────────┐
│             Skill Package            │
├─────────────────────────────────────┤
│  SKILL.md (required)                │
│  ├── YAML frontmatter (name, desc)  │
│  └── Markdown instructions          │
├─────────────────────────────────────┤
│  scripts/ (optional)                │
│  ├── Executable code                │
│  └── Tests                          │
├─────────────────────────────────────┤
│  references/ (optional)             │
│  └── Documentation chunks           │
├─────────────────────────────────────┤
│  assets/ (optional)                 │
│  └── Templates, images, fonts       │
└─────────────────────────────────────┘
```

### Agents Layer

Agents are specialized workers with defined responsibilities.

```
┌──────────────────────────────────────────────────────────────┐
│                      Agent Categories                         │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Orchestration          Planning            Quality          │
│  ┌────────────┐        ┌──────────┐       ┌─────────────┐  │
│  │implementer │        │brainstorm│       │code-reviewer│  │
│  │proj-manager│        │ planner  │       │   tester    │  │
│  └────────────┘        │researcher│       │  debugger   │  │
│                        └──────────┘       └─────────────┘  │
│                                                              │
│  Documentation         Specialized                           │
│  ┌────────────┐        ┌────────────────────────────────┐  │
│  │docs-manager│        │ui-ux-designer, database-admin, │  │
│  └────────────┘        │git-manager, scout, mcp-manager,│  │
│                        │copywriter, journal-writer      │  │
│                        └────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

### Workflows Layer

Workflows define execution patterns and coordination.

```
┌─────────────────────────────────────────────────────────────┐
│                    Workflow Patterns                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Sequential:  A ──► B ──► C ──► D                          │
│                                                             │
│  Parallel:    ┌─► B ─┐                                     │
│               A ─┼─► C ─┼─► E                               │
│               └─► D ─┘                                     │
│                                                             │
│  Loop:        A ──► B ──► C ──┐                            │
│                     ▲         │ (fail)                     │
│                     └─────────┘                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow

### Implementation Flow

```
User Request
     │
     ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ brainstormer│───►│   planner   │───►│ implementer │
│  (optional) │    │             │    │             │
└─────────────┘    └─────────────┘    └──────┬──────┘
                                             │
                   ┌─────────────────────────┼─────────────────────────┐
                   │                         │                         │
                   ▼                         ▼                         ▼
            ┌───────────┐            ┌───────────┐            ┌───────────┐
            │  tester   │◄──────────►│ debugger  │            │ui-designer│
            └───────────┘            └───────────┘            └───────────┘
                   │
                   ▼
            ┌─────────────┐
            │code-reviewer│
            └─────────────┘
                   │
         ┌─────────┴─────────┐
         ▼                   ▼
┌─────────────────┐  ┌─────────────┐
│ project-manager │  │ docs-manager│
└─────────────────┘  └─────────────┘
         │                   │
         ▼                   ▼
    ./plans/            ./docs/
```

### Report Handoff

```
Agent A                          Agent B
   │                                │
   │  ./plans/<plan>/reports/       │
   │  YYMMDD-A-to-B-task.md         │
   ├───────────────────────────────►│
   │                                │
```

## Storage Architecture

### Plans Directory
```
./plans/
└── YYYYMMDD-HHmm-<name>/
    ├── plan.md           # Master plan, links to phases
    ├── phase-01-*.md     # Phase details
    ├── phase-02-*.md
    └── reports/
        └── *.md          # Inter-agent communication
```

### Docs Directory
```
./docs/
├── project-overview-pdr.md    # Requirements
├── project-roadmap.md         # Timeline, changelog
├── code-standards.md          # Conventions
├── system-architecture.md     # This file
├── codebase-summary.md        # Generated by repomix
└── api-docs.md                # API reference (if applicable)
```

## Integration Points

### External Tools
- **repomix**: Codebase compaction for context
- **git**: Version control operations
- **psql/sqlcmd**: Database queries
- **MCP servers**: Extended capabilities

### Environment
- `.env` files for configuration
- Precedence: runtime > skill > parent

## Scalability Considerations

| Concern | Solution |
|---------|----------|
| Context limits | 100-line file limits, progressive disclosure |
| Agent confusion | Single responsibility, clear handoffs |
| Documentation drift | Trigger-based updates via docs-manager |
| Complex orchestration | Implementer as central coordinator |
