# Phase 6: Analyze

Cross-artifact consistency and quality validation (read-only).

## Purpose

Before implementation, verify:
- All requirements covered by tasks
- Plan aligns with constitution
- No conflicts between documents
- No missing dependencies

## Analysis Process

1. **Read All Documents**
   - Constitution
   - Specification
   - Plan
   - Data model
   - Tasks

2. **Coverage Check**

```bash
# Extract requirements
grep -E "R[0-9]+\.[0-9]+" spec.md | sort -u > requirements.txt

# Extract referenced requirements in tasks
grep -E "Requirement.*R[0-9]+" tasks.md | sort -u > covered.txt

# Compare
comm -23 requirements.txt covered.txt
```

3. **Consistency Checks**

**Constitution Alignment**:
- Does plan follow stated principles?
- Are architecture choices justified per constitution?

**Requirement Coverage**:
- Is every requirement addressed in tasks?
- Are acceptance criteria testable?

**Technical Coherence**:
- Do data models match spec needs?
- Do API contracts align with plan?
- Are dependencies realistic?

**Task Dependencies**:
- Are all dependencies valid?
- Is critical path identified?
- Any circular dependencies?

4. **Report Findings**

```markdown
# Analysis Report

## ✅ Passing Checks

- All requirements covered
- Constitution alignment verified
- No circular dependencies

## ⚠️ Warnings

- Requirement R3.4 has no corresponding task
- Task 5.2 references undefined dependency

## 🔴 Critical Issues

None found

## Recommendations

1. Add task for Requirement R3.4
2. Clarify dependency for task 5.2
3. Consider breaking task 6.1 into smaller tasks (estimated 8 hours)
```

## Guidelines

- **Read-only**: Don't modify documents
- **Objective**: Report facts, not opinions
- **Actionable**: Provide specific recommendations
- **Prioritized**: Critical issues first
