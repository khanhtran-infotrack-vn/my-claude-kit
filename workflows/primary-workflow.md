# Primary Workflow

**IMPORTANT:** Analyze the skills catalog and activate the skills that are needed for the task during the process.
**IMPORTANT**: Ensure token efficiency while maintaining high quality.

#### 0. Discovery (Optional)
**When requirements are unclear or architectural decisions need exploration:**
- Delegate to `brainstormer` agent to:
  - Explore multiple solution approaches with pros/cons
  - Debate technical trade-offs and challenge assumptions
  - Validate feasibility and consider all stakeholders
  - Create a comprehensive markdown summary report with recommended solution
  - Generate INVEST-compliant user stories with acceptance criteria and time estimates
  - Save user story report to `./docs/user-stories/YYMMDD-HHmm-epic-name.md`
- **Note:** brainstormer provides advisory only - does NOT implement

#### 1. Code Implementation

**For Backend Development - Test-First Mandatory:**
- **ALWAYS follow Test-First Development (TFD)** for backend code
- **Workflow:** Write failing tests → Implement minimal code → Refactor while green
- **Coverage:** All handlers, validators, domain logic
- **NO "Arrange/Act/Assert" comments** - write clean, self-documenting tests

**General Implementation:**
- Before you start, delegate to `planner` agent to create a implementation plan with TODO tasks in `./plans` directory.
- When in planning phase, use multiple `researcher` agents in parallel to conduct research on different relevant technical topics and report back to `planner` agent to create implementation plan.
- Write clean, readable, and maintainable code
- Follow established architectural patterns
- Implement features according to specifications
- Handle edge cases and error scenarios
- **DO NOT** create new enhanced files, update to the existing files directly.
- **[IMPORTANT]** After creating or modifying code file, run compile command/script to check for any compile errors.
- For .NET projects: Run `dotnet build` after code changes to verify compilation

#### 2. Testing
- **Backend code MUST use Test-First Development** - tests written BEFORE implementation
- Delegate to `tester` agent to run tests and analyze the summary report.
  - Write comprehensive unit tests
  - Ensure high code coverage (70% unit, 20% integration, 10% E2E)
  - Test error scenarios and edge cases
  - Validate performance requirements
- Tests are critical for ensuring code quality and reliability, **DO NOT** ignore failing tests just to pass the build.
- **IMPORTANT:** make sure you don't use fake data, mocks, cheats, tricks, temporary solutions, just to pass the build or github actions.
- **IMPORTANT:** Always fix failing tests follow the recommendations and delegate to `tester` agent to run tests again, only finish your session when all tests pass.

#### 3. Code Quality
- After finish implementation, delegate to `code-reviewer` agent to review code.
- Follow coding standards and conventions
- Write self-documenting code
- Add meaningful comments for complex logic
- Optimize for performance and maintainability

#### 4. Integration
- Always follow the plan given by `planner` agent
- Ensure seamless integration with existing code
- Follow API contracts precisely
- Maintain backward compatibility
- Document breaking changes
- Delegate to `docs-manager` agent to update docs in `./docs` directory if any.

#### 5. Debugging
- When a user report bugs or issues on the server or a CI/CD pipeline, delegate to `debugger` agent to run tests and analyze the summary report.
- Read the summary report from `debugger` agent and implement the fix.
- Delegate to `tester` agent to run tests and analyze the summary report.
- If the `tester` agent reports failed tests, fix them follow the recommendations and repeat from the **Step 2**.