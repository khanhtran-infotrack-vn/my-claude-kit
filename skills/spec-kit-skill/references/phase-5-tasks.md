# Phase 5: Tasks

Generate dependency-ordered, actionable implementation tasks.

## Prerequisites Script

```bash
# Check prerequisites
.specify/scripts/bash/check-prerequisites.sh --json [--require-tasks] [--include-tasks]

# Output: {"FEATURE_DIR": "/path", "AVAILABLE_DOCS": ["spec.md", "plan.md", ...]}
```

## Task Generation

Create `.specify/specs/NNN-feature/tasks.md`:

```markdown
# Implementation Tasks: [Feature Name]

## Phase 1: Foundation

- [ ] 1.1 Set up project structure
  - Create directory layout per architecture doc
  - Configure build tools
  - Initialize testing framework
  - **Depends on**: None
  - **Requirement**: R1.1

- [ ] 1.2 [P] Configure development environment
  - Set up linters and formatters
  - Configure CI/CD pipeline basics
  - **Depends on**: 1.1
  - **Requirement**: R1.2

## Phase 2: Core Implementation

- [ ] 2.1 Implement User model and persistence
  - Create User entity with validation
  - Implement repository pattern
  - Write unit tests
  - **Depends on**: 1.1
  - **Requirement**: R2.1, R2.3

- [ ] 2.2 [P] Implement Document model
  - Create Document entity
  - Define relationships with User
  - Write unit tests
  - **Depends on**: 1.1
  - **Requirement**: R2.2

- [ ] 2.3 Implement API endpoints
  - Create REST controllers
  - Add request/response validation
  - Write integration tests
  - **Depends on**: 2.1, 2.2
  - **Requirement**: R3.1, R3.2

[Continue with all phases...]

## Phase N: Integration & Testing

- [ ] N.1 End-to-end testing
  - Write E2E test scenarios
  - Test critical user paths
  - **Depends on**: [all previous]
  - **Requirement**: All

## Notes

- `[P]` indicates tasks that can be parallelized
- Always check dependencies before starting
- Reference requirements for acceptance criteria
```

## Task Characteristics

**Each task should**:
- Be specific and actionable
- Reference requirements (R1.1, R2.3, etc.)
- List dependencies
- Be completable in 1-4 hours
- Have clear acceptance criteria

**Task Types**:
- Implementation tasks (write code)
- Testing tasks (write tests)
- Configuration tasks (set up tools)
- Integration tasks (connect components)

**Exclude**:
- Deployment tasks
- User training
- Marketing activities
- Non-coding work

## Dependency Markers

- **None**: Can start immediately
- **1.1**: Must complete task 1.1 first
- **1.1, 2.2**: Must complete both first
- **[P]**: Can run in parallel with siblings
