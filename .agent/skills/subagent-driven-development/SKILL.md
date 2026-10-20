---
name: subagent-driven-development
description: Development using multiple specialized subagents with review checkpoints and task decomposition
---

# Subagent-Driven Development

## Overview

Execute complex development tasks by decomposing them into modular sub-tasks, delegating to specialized subagents, and verifying results at defined checkpoints.

## Workflow

### 1. Task Decomposition
- Break the high-level goal into independent units of work (e.g., Schema & Models -> API Endpoints -> UI Templates -> Test Suite).
- Define clear input/output expectations for each step.

### 2. Subagent Dispatch
- Delegate isolated subtasks to subagents (e.g. `research` for codebase surveying, `self` for independent implementation branches).
- Ensure each agent has focused context and a single clear objective.

### 3. Review Checkpoints
- Inspect outputs from subagents before integrating into the main project branch.
- Run automated tests and code checks at each boundary.

### 4. Integration & Polish
- Merge changes, resolve any interface mismatches, and run full test suite.
