# AGENTS.md — ITHUTIR Agent OS

## Scope

These are common operational rules for agents working in this repository. Read `CONSTITUTION.md` first. Role-specific instructions may specialize these rules but must not contradict higher-level governance or safety requirements.

## Core behavior

1. Understand the goal before changing files.
2. Work in small, verifiable steps.
3. Prefer structured inputs/outputs between Brain, Orchestrator and Executors.
4. Do not hard-code a specific LLM, CLI agent or GUI engine into Orchestrator core.
5. Reuse provider/executor interfaces and adapters.
6. Do not create large empty scaffolding merely to resemble a target architecture; add modules with working functionality and tests.
7. Never treat an Executor's `done` response as proof of success. Validate.
8. Preserve project isolation and context boundaries.
9. Preserve human control for high-impact actions.

## Git safety

Before modifications, inspect repository/branch/working-tree state where available.

Do not autonomously:
- delete unrelated work;
- rewrite history;
- force push;
- push or deploy unless explicitly permitted;
- switch branches when it may discard work;
- commit secrets or runtime credentials.

Show/record meaningful diffs and validation results.

## File safety

- Read before replacing an existing file.
- Make the smallest complete change.
- Do not delete files unless the Task and permissions explicitly require it.
- Do not modify unrelated files.
- Task attachments are not automatically project source files and must not be committed without a reason.

## Execution

Executors should receive small concrete Steps with constraints, relevant context and verification criteria.

Failures must produce structured evidence such as stderr, traceback, test output, build output, diff or observed GUI state. Retry loops must be bounded by `max_attempts` and transition to `NEEDS_INPUT` or `FAILED` when exhausted.

## Computer Agent

Computer Agent is an Executor, not the Brain. Use a state-aware loop:

`SEE -> PLAN/THINK -> ACT -> VERIFY -> SEE`

Do not build it as a fixed-coordinate autoclicker. Prefer reliable API/connectors over GUI automation when appropriate. Mouse/keyboard, network, uploads/publication, destructive actions and privileged operations require explicit permission policy.

## Secrets

Never store API keys, tokens, passwords or credentials in source files, ordinary JSON configuration, logs or Git. Use an OS-backed secret store/keyring when implemented.

## Definition of Done

A Step is complete only when its acceptance/verification criteria pass. A Task is complete only when required Steps and validations pass and its resulting artifacts/state are recorded appropriately.
