# Phase 3: Clarify

Resolve underspecified areas through targeted questioning.

## Purpose

Before planning implementation, ensure specification is complete and unambiguous.

## Process

1. **Analyze Specification**
   - Read spec.md thoroughly
   - Identify ambiguities, gaps, assumptions
   - Note areas with multiple valid interpretations

2. **Generate Questions** (Maximum 5)
   - Prioritize high-impact areas
   - Focus on decisions that affect architecture
   - Ask about edge cases and error handling

3. **Question Format**

```markdown
## Clarifications

### Q1: [Clear, specific question]

**Context**: [Why this matters]
**Options**: [If multiple approaches exist]

### Q2: [Clear, specific question]

**Context**: [Why this matters]
**Impact**: [What decisions depend on this]
```

4. **Update Specification**
   - Add "## Clarifications" section to spec.md
   - Document questions and answers
   - Update relevant sections based on answers
   - Iterate until all critical questions answered

## Guidelines

- **Maximum 5 questions** per round
- **Specific, not general**: "How should we handle concurrent edits?" not "How should it work?"
- **Decision-focused**: Questions that inform technical choices
- **Incremental**: Can run multiple clarification rounds

## Example Questions

```markdown
## Clarifications

### Q1: How should the system handle conflicts when two users edit the same document simultaneously?

**Context**: This affects data model design and user experience.
**Options**:
- Last-write-wins (simple, may lose data)
- Operational transforms (complex, preserves all edits)
- Locked editing (simple, limits collaboration)

**Answer**: [User provides answer]

### Q2: What's the maximum number of concurrent users we need to support?

**Context**: Affects infrastructure planning and architecture decisions.
**Impact**: Determines caching strategy, database choices, and scaling approach.

**Answer**: [User provides answer]
```
