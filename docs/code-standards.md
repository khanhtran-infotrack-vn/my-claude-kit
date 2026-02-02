# Code Standards

## Core Principles

| Principle | Description |
|-----------|-------------|
| **YAGNI** | You Aren't Gonna Need It - don't add functionality until necessary |
| **KISS** | Keep It Simple, Stupid - prefer simple solutions |
| **DRY** | Don't Repeat Yourself - extract common patterns |
| **SOLID** | Single responsibility, Open-closed, Liskov substitution, Interface segregation, Dependency inversion |

## File Organization

### Skills
```
skills/<skill-name>/
├── SKILL.md              # Required, <100 lines
├── scripts/              # Optional executables
│   ├── main.py          # or main.js
│   └── test_main.py     # Required if scripts exist
├── references/           # Optional docs (<100 lines each)
└── assets/              # Optional templates/images
```

### Agents
```
agents/<agent-name>.md    # YAML frontmatter + instructions
```

### Plans
```
plans/YYYYMMDD-HHmm-<name>/
├── plan.md              # Overview, <80 lines
├── phase-XX-<name>.md   # Phase details
└── reports/             # Agent handoff reports
```

## Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Skill folders | kebab-case | `chrome-devtools` |
| Agent files | kebab-case | `code-reviewer.md` |
| Plan folders | timestamp-kebab | `20250202-1430-auth-feature` |
| Report files | date-from-to-task | `250202-tester-debugger-auth-report.md` |
| Scripts | snake_case (Python), camelCase (JS) | `fetch_data.py`, `fetchData.js` |

## SKILL.md Format

```yaml
---
name: skill-name
description: Brief description of the skill
---

Markdown instructions here (under 100 lines total)
```

## Agent Definition Format

```yaml
---
name: agent-name
description: When to use this agent with examples
model: sonnet|haiku|default  # Optional
tools: Tool1, Tool2          # Optional, restricts available tools
---

Agent instructions and responsibilities
```

## Script Requirements

### Python
- Include `if __name__ == "__main__":` block
- Add corresponding `test_*.py` file
- Use type hints
- Handle environment variables via `.env`

### Node.js
- Use ES modules or CommonJS consistently
- Include test file
- Use TypeScript when complexity warrants
- Handle environment variables via dotenv

## Environment Variables

Precedence (highest to lowest):
1. `process.env` (runtime)
2. Skill-level `.env`
3. Parent directory `.env`

## Documentation Standards

### Markdown
- Use ATX headers (`#`, `##`, `###`)
- Include table of contents for files >50 lines
- Use fenced code blocks with language tags
- Keep lines under 100 characters when possible

### Comments
- Explain "why" not "what"
- Add comments for complex logic only
- Use JSDoc/docstrings for public APIs

## Token Efficiency

- Keep SKILL.md under 100 lines
- Split large references into multiple files
- Use progressive disclosure (basic → advanced)
- Sacrifice grammar for concision in reports
- Avoid redundant context in agent handoffs

## Quality Gates

Before merging:
- [ ] Scripts have tests
- [ ] SKILL.md under 100 lines
- [ ] Agent has clear examples in description
- [ ] No hardcoded secrets
- [ ] Cross-platform compatible (no bash-only scripts)
