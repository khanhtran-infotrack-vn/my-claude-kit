---
name: repomix
description: Package entire code repositories into single AI-friendly files using Repomix. Capabilities include pack codebases with customizable include/exclude patterns, generate multiple output formats (XML, Markdown, plain text), preserve file structure and context, optimize for AI consumption with token counting, filter by file types and directories, add custom headers and summaries. Use when packaging codebases for AI analysis, creating repository snapshots for LLM context, analyzing third-party libraries, preparing for security audits, generating documentation context, or evaluating unfamiliar codebases.
---

# Repomix Skill

Package repositories into single AI-friendly files for LLM analysis.

## Quick Start

```bash
# Install
npm install -g repomix  # or: brew install repomix

# Package current directory (generates repomix-output.xml)
repomix

# Common patterns
repomix --style markdown                    # Output as markdown
repomix --include "src/**/*.ts" -o out.md   # Filter + custom output
repomix --remote owner/repo                 # Package remote repo
repomix --remove-comments --copy            # Clean + copy to clipboard
```

## When to Use

- Packaging codebases for AI analysis
- Creating repository snapshots for LLM context
- Analyzing third-party libraries
- Security audit preparation
- Documentation context generation

## Output Formats

| Format | Flag | Best For |
|--------|------|----------|
| XML | `--style xml` | Structured parsing (default) |
| Markdown | `--style markdown` | Human-readable |
| JSON | `--style json` | Programmatic processing |
| Plain | `--style plain` | Simple text |

## Common Commands

```bash
# File selection
repomix --include "src/**/*.ts,*.md"    # Include patterns
repomix -i "tests/**,*.test.js"         # Ignore patterns

# Remote repositories
npx repomix --remote yamadashy/repomix
npx repomix --remote https://github.com/owner/repo/commit/hash

# Token optimization
repomix --token-count-tree              # Show token distribution
repomix --token-count-tree 1000         # Files with 1000+ tokens only
repomix --remove-comments               # Strip comments (~70% reduction)
```

## Token Limits Reference

- Claude Sonnet 4.5: ~200K tokens
- GPT-4: ~128K tokens
- GPT-3.5: ~16K tokens

## Security

Repomix uses Secretlint to detect sensitive data. Best practices:
- Review output before sharing
- Use `.repomixignore` for sensitive files
- Avoid packaging `.env` files
- Disable checks if needed: `repomix --no-security-check`

## Reference Documentation

| Document | Description |
|----------|-------------|
| [configuration.md](references/configuration.md) | Config files, patterns, output formats |
| [usage-patterns.md](references/usage-patterns.md) | AI analysis, security audits, docs generation |

## Resources

- GitHub: https://github.com/yamadashy/repomix
- Docs: https://repomix.com/guide/
