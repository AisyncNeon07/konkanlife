---
name: systematic-debugging
description: Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes
---

# Systematic Debugging

## Overview

**Core principle:** ALWAYS find root cause before attempting fixes. Symptom fixes are failure.

**The Iron Law:**
```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

## The Four Phases

You MUST complete each phase before proceeding to the next.

### Phase 1: Root Cause Investigation
1. **Read Error Messages Carefully**: Note error types, stack traces, and line numbers.
2. **Reproduce the Issue**: Create a minimal reproduction script or failing unit test.
3. **Trace the Data Flow**: Follow inputs from entry points down to where the error manifests.
4. **Isolate the Fault**: Distinguish root cause from secondary symptoms.

### Phase 2: Pattern Analysis
1. Check recent code changes (git diff or commits).
2. Compare against working components or test cases.
3. Verify assumptions against actual runtime state.

### Phase 3: Hypothesis & Verification
1. Formulate a single, testable hypothesis for why the issue occurs.
2. Test hypothesis with minimal diagnostic logging or assertions.

### Phase 4: Implementation & Regression Prevention
1. Apply the minimal targeted fix addressing the root cause.
2. Run test suite to verify the fix.
3. Add regression tests to prevent recurrence.
