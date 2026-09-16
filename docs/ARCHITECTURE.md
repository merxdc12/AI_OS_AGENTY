# ITHUTIR Agent OS — Target Architecture

## Core model

```text
User / Task Sources
       |
       v
Task Intake -> Inbox -> Context Manager
       |
       v
Python Orchestrator
       |
       +---- BrainProvider ------> LLM Brain
       |
       +---- ExecutorProvider ---> CLI Executor (Codex/Gemini/future)
       |
       +---- ComputerExecutor ---> Linux GUI / Browser
       |
       +---- API/Connector ------> External services
       |
       v
Validation -> Review -> Fix/Retry -> State/Memory -> Git/Artifacts
```

## Principle

`LLM = Brain, Python = Orchestrator, Executor = concrete action, Validation = objective feedback.`

Brain and Executor are independent selections. Orchestrator core must not contain vendor-specific assumptions.

## Unified task pipeline

`Intake -> Inbox -> Context -> Brain -> Structured Plan -> Task Queue -> Executor -> Validation -> Review -> Fix/Retry -> Git/Artifacts -> Project Memory -> Done`

## Task sources

- PyQt6 Control Center;
- CLI;
- GitHub Issues (explicit `agent-ready` opt-in for automatic execution);
- files/folders/attachments;
- future connectors.

All sources normalize into one internal Task model.

## Computer Agent

Computer Agent is a GUI Executor for Linux/browser workflows. Its feedback loop is:

`SEE -> THINK/PLAN -> ACT -> VERIFY -> SEE`

Target capabilities: screen capture, visual target selection, mouse, keyboard, waits/state transitions, verification, structured observations/results. It must not rely solely on fixed coordinates.

When a reliable direct API/connector exists, Orchestrator should be able to prefer it over GUI automation.

## State

Runtime State and Project Memory are separate.

Runtime State stores current task, step, attempt, errors, validation and recovery position.
Project Memory stores architecture decisions, conventions, dependencies, rejected alternatives, lessons and previous results.

## Permissions

Least privilege. Permissions should cover file reads/writes, tests/builds, Git, network, package installation, deletion, mouse/keyboard, browser actions, upload/publish and privileged commands. High-impact actions require policy/human approval where appropriate.

## GUI boundary

PyQt6 Control Center communicates with Orchestrator API only. It does not directly manage Codex, Gemini or Computer Agent.
