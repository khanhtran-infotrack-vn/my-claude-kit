# Phase Detection Logic

Before proceeding, always detect the current state.

## 1. CLI Installed?

```bash
if command -v specify &> /dev/null || [ -x "$HOME/.local/bin/specify" ]; then
  echo "CLI installed"
else
  echo "CLI not installed - guide user through installation"
fi
```

## 2. Project Initialized?

```bash
if [ -d ".specify" ] && [ -f ".specify/memory/constitution.md" ]; then
  echo "Project initialized"
else
  echo "Project not initialized - guide user through 'specify init'"
fi
```

## 3. Current Feature

```bash
# Get latest feature directory
LATEST=$(ls -d .specify/specs/[0-9]* 2>/dev/null | sort -V | tail -1)
echo "Latest feature: $LATEST"
```

## 4. Current Phase

Detect phase by checking file existence in latest feature:

```bash
FEATURE_DIR=".specify/specs/001-feature-name"

if [ ! -f ".specify/memory/constitution.md" ]; then
  echo "Phase: constitution"
elif [ ! -d "$FEATURE_DIR" ]; then
  echo "Phase: specify"
elif [ -f "$FEATURE_DIR/spec.md" ] && ! grep -q "## Clarifications" "$FEATURE_DIR/spec.md"; then
  echo "Phase: clarify"
elif [ ! -f "$FEATURE_DIR/plan.md" ]; then
  echo "Phase: plan"
elif [ ! -f "$FEATURE_DIR/tasks.md" ]; then
  echo "Phase: tasks"
elif [ -f "$FEATURE_DIR/tasks.md" ] && grep -q "\\- \\[ \\]" "$FEATURE_DIR/tasks.md"; then
  echo "Phase: implement"
else
  echo "Phase: complete"
fi
```
