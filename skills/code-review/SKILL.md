---
name: code-review
description: Use when receiving code review feedback (especially if unclear or technically questionable), when completing tasks or major features requiring review before proceeding, or before making any completion/success claims. Covers three practices - receiving feedback with technical rigor over performative agreement, requesting reviews via code-reviewer subagent, and verification gates requiring evidence before any status claims. Essential for subagent-driven development, pull requests, and preventing false completion claims.
---

# Code Review

Technical rigor, evidence-based claims, and verification over performative responses.

## Core Principle

**Technical correctness over social comfort.** Verify before implementing. Ask before assuming. Evidence before claims.

Always honor **YAGNI**, **KISS**, **DRY**, **SOLID**. Be honest, brutal, straight to the point, concise.

## Three Practices

### 1. Receiving Feedback

**Trigger:** Receiving review comments, unclear feedback, feedback conflicts with decisions

**Pattern:** READ → UNDERSTAND → VERIFY → EVALUATE → RESPOND → IMPLEMENT

**Rules:**
- ❌ No performative agreement ("You're right!", "Great point!")
- ❌ No implementation before verification
- ✅ Restate requirement, ask questions, push back technically
- ✅ YAGNI check: grep for usage before implementing "proper" features

**Reference:** `references/code-review-reception.md`

### 2. Requesting Review

**Trigger:** After each task, major features, before merge

**Process:**
```bash
BASE_SHA=$(git rev-parse HEAD~1)
HEAD_SHA=$(git rev-parse HEAD)
```
Dispatch code-reviewer subagent with: WHAT_IMPLEMENTED, PLAN, BASE_SHA, HEAD_SHA

**Reference:** `references/requesting-code-review.md`

### 3. Verification Gates

**Trigger:** Before ANY completion/success claims

**Iron Law:** NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE

**Gate:** IDENTIFY command → RUN command → READ output → VERIFY confirms claim → THEN claim

**Requirements:**
- Tests pass: Output shows 0 failures
- Build succeeds: Exit code 0
- Bug fixed: Original symptom test passes

**Red Flags - STOP:** Using "should"/"probably"/"seems", satisfaction before verification, committing without verification

**Reference:** `references/verification-before-completion.md`

## Quick Decision Tree

```
SITUATION?
├─ Received feedback
│  ├─ Unclear? → STOP, ask clarification
│  └─ From external? → Verify technically before implementing
├─ Completed work
│  └─ Major feature? → Request code-reviewer subagent
└─ About to claim status
   ├─ Have fresh verification? → Claim WITH evidence
   └─ No verification? → RUN verification first
```

## Bottom Line

1. Technical rigor over social performance
2. Systematic review via code-reviewer subagent
3. Evidence before claims - verification gates always

**Verify. Question. Then implement. Evidence. Then claim.**
