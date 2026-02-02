# Phase 2: Specify

Define *what* needs building and *why*, avoiding technology specifics.

## Script Usage

```bash
# Create new feature
.specify/scripts/bash/create-new-feature.sh --json "feature-name"

# Expected JSON output:
# {"BRANCH_NAME": "001-feature-name", "SPEC_FILE": "/path/to/.specify/specs/001-feature-name/spec.md"}
```

**Parse JSON**: Extract `BRANCH_NAME` and `SPEC_FILE` for subsequent operations.

## Template Structure

Load `.specify/templates/spec-template.md` to understand required sections, then create specification at `SPEC_FILE` location.

## Specification Content

Focus on **functional requirements**:

```markdown
# Feature Specification: [Feature Name]

## Problem Statement

[What problem are we solving?]

## User Stories

### Story 1: [Title]

As a [role]
I want [capability]
So that [benefit]

**Acceptance Criteria:**
- [ ] [Specific, testable criterion]
- [ ] [Specific, testable criterion]

### Story 2: [Title]

[Continue...]

## Non-Functional Requirements

- Performance: [Specific metrics]
- Security: [Requirements]
- Accessibility: [Standards]
- Scalability: [Expectations]

## Success Metrics

- [Measurable outcome]
- [Measurable outcome]

## Out of Scope

[Explicitly state what's NOT included]
```

## Key Principles

- **Technology-agnostic**: Don't specify "use React" or "MySQL"
- **Outcome-focused**: Describe what user achieves, not how
- **Testable**: Acceptance criteria must be verifiable
- **Complete**: Address edge cases and error scenarios

## Git Integration

The script automatically:
- Creates new feature branch (e.g., `001-feature-name`)
- Checks out the branch
- Initializes spec file
