---
name: template-skill
description: Template for creating new Claude Code skills. Copy this folder structure to start a new skill. Contains placeholder SKILL.md with required frontmatter format and optional directories (scripts/, references/, assets/) for bundled resources.
---

# Skill Template

This is a template for creating new skills. Copy this folder to create a new skill.

## Required Structure

```
skill-name/
├── SKILL.md (required)         # Main skill file with YAML frontmatter
├── scripts/                    # Optional: executable Python/Bash code
├── references/                 # Optional: documentation to load as needed
└── assets/                     # Optional: templates, images, fonts for output
```

## SKILL.md Format

The frontmatter must contain:
- `name`: Skill name (kebab-case)
- `description`: What the skill does AND when to use it (triggers)

The body contains instructions for using the skill.

## Creating a New Skill

1. Copy this folder with your skill name
2. Update the frontmatter name and description
3. Add instructions in the body
4. Add scripts/, references/, assets/ as needed
5. Keep SKILL.md under 500 lines (use references/ for details)
