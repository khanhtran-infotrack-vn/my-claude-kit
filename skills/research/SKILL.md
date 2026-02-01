---
name: research
description: Use when you need to research, analyze, and plan technical solutions that are scalable, secure, and maintainable.
---

# Research

Systematic research methodology for technical solutions.

## Principles

Always honor **YAGNI**, **KISS**, **DRY**, **SOLID**.
**Be honest, brutal, straight to the point, concise.**

## Phases

### 1. Scope Definition
- Identify key terms and concepts
- Determine recency requirements
- Establish evaluation criteria
- Set research depth boundaries

### 2. Information Gathering

**Search Strategy** (max 5 researches):
```bash
# Primary: Gemini CLI (if available)
gemini -m gemini-2.5-flash -p "...search prompt..."
# Fallback: WebSearch tool
```
- Save outputs to `./plans/<plan-name>/reports/YYMMDD-<topic>.md`
- Include "best practices", "2024", "security", "performance"
- Prioritize official docs, GitHub repos, authoritative blogs

**Deep Analysis:**
- Use `docs-seeker` skill for GitHub repos
- Focus on official docs, README files, changelogs

**Cross-Reference:**
- Verify across multiple sources
- Check publication dates
- Identify consensus vs controversial approaches

### 3. Analysis & Synthesis
- Identify patterns and best practices
- Evaluate pros/cons of approaches
- Assess technology maturity
- Recognize security/performance implications

### 4. Report Generation

Save to: `./plans/<plan-name>/reports/YYMMDD-<topic>.md`

```markdown
# Research Report: [Topic]

## Executive Summary
[2-3 paragraph overview]

## Key Findings
### Technology Overview
### Current State & Trends
### Best Practices
### Security Considerations
### Performance Insights

## Implementation Recommendations
### Quick Start Guide
### Code Examples
### Common Pitfalls

## Resources & References
- Official Documentation
- Recommended Tutorials
- Community Resources
```

## Quality Standards

- **Accuracy**: Verified across multiple sources
- **Currency**: Prioritize last 12 months
- **Actionability**: Practical, implementable
- **Attribution**: Always cite sources

## Special Considerations

- Check recent CVEs for security topics
- Look for benchmarks for performance research
- Assess community adoption for new technologies
- Verify API availability and auth requirements
- Note deprecation warnings and migration paths

**IMPORTANT:** Sacrifice grammar for concision. List unresolved questions at end.
