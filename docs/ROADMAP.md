# ITHUTIR Agent OS — Master Roadmap

## Completed foundation

- **Lab 01** — local initial Orchestrator prototype: Python -> Codex CLI. Existing real local code must be imported from the development PC after comparison; do not recreate it from assumptions.

## Next

- **Lab 01.5 — Governance Foundation**
  - canonical `CONSTITUTION.md`;
  - root `AGENTS.md`;
  - rule precedence;
  - governance checkpoint.

- **Lab 02 — Brain + Executor interfaces**
  - `BrainProvider`;
  - `ExecutorProvider`;
  - wrap current Codex CLI as `CodexExecutor`;
  - first Brain adapter;
  - `Task -> Brain -> Plan -> Executor -> Result`;
  - safe integration test.

## Core implementation

- **Lab 03** — Task Model.
- **Lab 04** — Task Intake + Inbox.
- **Lab 05** — CLI Intake.
- **Lab 06** — Structured Task Plan.
- **Lab 07** — State Machine + persistence.
- **Lab 08** — Project Manager / project isolation.
- **Lab 09** — New Project Intake.
- **Lab 10** — Attachments.
- **Lab 11** — Context Manager + Auto Collect.
- **Lab 12** — GitHub Issues Intake (`agent-ready`).
- **Lab 13** — Agent Roles: Architect / Developer / Tester / Debugger / Reviewer.
- **Lab 14** — Validation Engine.
- **Lab 15** — Feedback / Debug loop + bounded `max_attempts`.
- **Lab 16** — Git Safety Layer.
- **Lab 17** — Permissions / approvals / least privilege.
- **Lab 18** — Project Memory.
- **Lab 19** — Task Queue / dependencies / priorities.
- **Lab 20** — Recovery / resume after restart.

## Desktop Control Center

- **Lab 21** — PyQt6 Core GUI.
- **Lab 22** — GUI Inbox / Projects / Files / Context.
- **Lab 23** — GUI Execution / Git / Tests / live logs.
- **Lab 24** — Integration / E2E tests.
- **Lab 25** — ITHUTIR Agent OS v1.0 stabilization.

## Computer Agent track

Computer Agent development starts after the generic Task/State/Executor/Permissions/Validation framework is stable enough to reuse.

1. Computer Agent Foundation / `ComputerExecutor` interface.
2. Screen Capture.
3. Visual Understanding / target selection.
4. Mouse actions.
5. Keyboard actions.
6. SEE/ACT/VERIFY loop.
7. Browser navigation.
8. Computer permissions and emergency Stop/Pause.
9. Orchestrator integration.
10. Real browser/Canva-style workflow test.

Computer Agent is not a separate automation architecture. It must reuse common Task, State, Context, Permissions, Validation, Logging and Recovery infrastructure.

## Definition of Done for Lab 02

Orchestrator no longer directly depends on a specific LLM or Codex CLI. Brain and Executor are replaceable through standardized interfaces, and the current Codex path still works through its adapter.

## Engineering rule

Build in small verified increments:

`UNDERSTAND -> IMPLEMENT -> RUN -> VERIFY -> CHECKPOINT -> NEXT`

Do not create an empty full architecture in advance. Add real modules as functionality is implemented.
