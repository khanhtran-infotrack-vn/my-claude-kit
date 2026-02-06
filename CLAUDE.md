# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a collection of Claude Code Skills, Agents, and Workflows. Skills are modular packages that extend Claude's capabilities with specialized knowledge, workflows, and tool integrations.

## Structure

```
├── opencode/
│   └── agents/      # Subagent definitions (scout, tester, planner, etc.)
├── skills/          # Skill packages with SKILL.md + optional scripts/references/assets
│   └── document-skills/  # Document manipulation skills (pdf, docx, pptx, xlsx)
└── workflows/       # Orchestration protocols and development guidelines
```

## Skill Anatomy

Each skill contains:
- `SKILL.md` (required) - YAML frontmatter (name, description) + markdown instructions
- `scripts/` (optional) - Executable Python/Node.js code
- `references/` (optional) - Documentation loaded into context as needed
- `assets/` (optional) - Templates, images, fonts used in output

## Key Constraints

- SKILL.md must be under 100 lines; split larger content into references/
- Referenced markdown files also under 100 lines (progressive disclosure)
- Scripts must include tests and respect `.env` precedence: `process.env` > skill `.env` > parent `.env`
- Prefer Node.js or Python scripts over bash for cross-platform compatibility

## Creating Skills

Initialize new skill:
```bash
scripts/init_skill.py <skill-name> --path <output-directory>
```

Package skill for distribution:
```bash
scripts/package_skill.py <path/to/skill-folder>
```

## Agent Orchestration

- **Sequential chaining**: Planning → Implementation → Testing → Review
- **Parallel execution**: Independent tasks (code + tests + docs) can run simultaneously
- Key agents: `planner`, `tester`, `code-reviewer`, `docs-manager`, `debugger`, `scout`

## Writing Style

Use imperative/infinitive form in skill instructions (e.g., "To accomplish X, do Y" not "You should do X").
