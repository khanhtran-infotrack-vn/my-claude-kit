---
name: spec-kit-skill
description: GitHub Spec-Kit integration for constitution-based spec-driven development. 7-phase workflow. Triggers: "spec-kit", "speckit", "constitution", "specify", ".specify/", "规格驱动开发", "需求规格".
---

# Spec-Kit: Constitution-Based Spec-Driven Development

Official GitHub Spec-Kit integration providing a 7-phase constitution-driven workflow for feature development.

## Quick Start

This skill works with the [GitHub Spec-Kit CLI](https://github.com/github/spec-kit) to guide you through structured feature development:

1. **Constitution** → Establish governing principles
2. **Specify** → Define functional requirements
3. **Clarify** → Resolve ambiguities
4. **Plan** → Create technical strategy
5. **Tasks** → Generate actionable breakdown
6. **Analyze** → Validate consistency
7. **Implement** → Execute implementation

**Storage**: Creates files in `.specify/specs/NNN-feature-name/` directory with numbered features

## When to Use

- Setting up spec-kit in a project
- Creating constitution-based feature specifications
- Working with .specify/ directory
- Following GitHub spec-kit workflow
- Constitution-driven development

---

## Prerequisites & Setup

### Check CLI Installation

First, verify if spec-kit CLI is installed:

```bash
command -v specify || echo "Not installed"
```

### Installation

If not installed:

```bash
# Persistent installation (recommended)
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git

# One-time usage
uvx --from git+https://github.com/github/spec-kit.git specify init <PROJECT_NAME>
```

**Requirements**:
- Python 3.11+
- Git
- uv package manager ([install uv](https://docs.astral.sh/uv/))

### Project Initialization

If CLI is installed but project not initialized:

```bash
# Initialize in current directory
specify init . --ai claude

# Initialize new project
specify init <project-name> --ai claude

# Options:
# --force: Overwrite non-empty directories
# --script ps: Generate PowerShell scripts (Windows)
# --no-git: Skip Git initialization
```

---

## Phase Reference

Load the appropriate reference file based on your current phase:

| Phase | Reference File | Purpose |
|-------|----------------|---------|
| Detection | [phase-detection.md](references/phase-detection.md) | Detect CLI/project/phase state |
| 1. Constitution | [phase-1-constitution.md](references/phase-1-constitution.md) | Establish governing principles |
| 2. Specify | [phase-2-specify.md](references/phase-2-specify.md) | Define functional requirements |
| 3. Clarify | [phase-3-clarify.md](references/phase-3-clarify.md) | Resolve ambiguities |
| 4. Plan | [phase-4-plan.md](references/phase-4-plan.md) | Create technical strategy |
| 5. Tasks | [phase-5-tasks.md](references/phase-5-tasks.md) | Generate actionable breakdown |
| 6. Analyze | [phase-6-analyze.md](references/phase-6-analyze.md) | Validate consistency |
| 7. Implement | [phase-7-implement.md](references/phase-7-implement.md) | Execute implementation |

---

## Phase Quick Reference

### Phase 1: Constitution
Create `.specify/memory/constitution.md` with project values, principles, technical standards, and decision frameworks. See [phase-1-constitution.md](references/phase-1-constitution.md).

### Phase 2: Specify
Run `.specify/scripts/bash/create-new-feature.sh --json "feature-name"` to create spec. Focus on functional requirements, avoid technology specifics. See [phase-2-specify.md](references/phase-2-specify.md).

### Phase 3: Clarify
Generate maximum 5 questions to resolve ambiguities. Add "## Clarifications" section to spec.md. See [phase-3-clarify.md](references/phase-3-clarify.md).

### Phase 4: Plan
Run `.specify/scripts/bash/setup-plan.sh --json`. Create plan.md, data-model.md, and API contracts. See [phase-4-plan.md](references/phase-4-plan.md).

### Phase 5: Tasks
Run `.specify/scripts/bash/check-prerequisites.sh --json`. Create tasks.md with dependency-ordered, actionable tasks. See [phase-5-tasks.md](references/phase-5-tasks.md).

### Phase 6: Analyze
Cross-artifact validation (read-only). Check requirement coverage, constitution alignment, consistency. See [phase-6-analyze.md](references/phase-6-analyze.md).

### Phase 7: Implement
Execute tasks phase-by-phase, respecting dependencies. Test-driven approach. See [phase-7-implement.md](references/phase-7-implement.md).

---

## File Structure

```
.specify/
├── memory/
│   └── constitution.md              # Phase 1
├── specs/
│   └── 001-feature-name/            # Numbered features
│       ├── spec.md                  # Phase 2
│       ├── plan.md                  # Phase 4
│       ├── data-model.md            # Phase 4
│       ├── contracts/               # Phase 4
│       │   ├── api-spec.json
│       │   └── signalr-spec.md
│       ├── research.md              # Phase 4 (optional)
│       ├── quickstart.md            # Phase 4 (optional)
│       └── tasks.md                 # Phase 5
├── scripts/
│   └── bash/
│       ├── check-prerequisites.sh
│       ├── create-new-feature.sh
│       ├── setup-plan.sh
│       └── common.sh
└── templates/
    ├── spec-template.md
    ├── plan-template.md
    └── tasks-template.md
```

## Workflow Rules

1. **Sequential Phases**: Must complete phases in order
2. **Constitution First**: Always establish constitution before features
3. **Branch per Feature**: Each feature gets its own Git branch
4. **Numbered Features**: Use sequential numbering (001, 002, 003)
5. **Script Integration**: Use provided bash scripts for consistency
6. **Principle-Driven**: All decisions align with constitution

## Summary

Spec-Kit provides a rigorous, constitution-based approach to feature development with clear phases, explicit dependencies, and comprehensive documentation at every step. The workflow ensures alignment from principles through implementation.

## Supporting Files

For advanced detection logic and automation scripts, see:
- [Detection Logic](helpers/detection-logic.md) - Comprehensive state detection algorithms
