# Phase 7: Implement

Execute tasks systematically, respecting dependencies and test-driven development.

## Implementation Strategy

1. **Phase-by-Phase Execution**
   - Complete all Phase 1 tasks before Phase 2
   - Respect task dependencies
   - Leverage parallel markers [P]

2. **Task Execution Pattern**

```bash
# For each task:
# 1. Read context
cat .specify/specs/001-feature/spec.md
cat .specify/specs/001-feature/plan.md
cat .specify/specs/001-feature/data-model.md

# 2. Check dependencies
# Verify all depends-on tasks are complete

# 3. Implement
# Write code per task description

# 4. Test
# Write and run tests

# 5. Validate
# Check against requirements

# 6. Mark complete
# Update tasks.md: - [x] task completed
```

3. **Test-Driven Approach**

For each task:
- Write tests first (when applicable)
- Implement to pass tests
- Refactor while maintaining green tests
- Integration test when connecting components

4. **Quality Checks**

Before marking task complete:
- [ ] Code follows plan architecture
- [ ] Tests written and passing
- [ ] Meets acceptance criteria
- [ ] No obvious bugs
- [ ] Integrated with previous work

## Handling Errors

If implementation reveals issues:

1. **Design Issues**: Return to plan phase, update plan
2. **Requirement Gaps**: Return to specify/clarify, update spec
3. **Technical Blockers**: Document, escalate to user

## Progress Tracking

Update tasks.md as you go:

```markdown
- [x] 1.1 Set up project structure ✓ Complete
- [x] 1.2 [P] Configure development environment ✓ Complete
- [ ] 2.1 Implement User model ← Currently here
- [ ] 2.2 [P] Implement Document model
```

## Completion Criteria

Feature is complete when:
- [ ] All tasks marked complete
- [ ] All tests passing
- [ ] All requirements validated
- [ ] Code reviewed (if applicable)
- [ ] Documentation updated
