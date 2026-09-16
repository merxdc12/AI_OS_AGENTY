# ITHUTIR Agent OS / AI_OS_AGENTY

Dedicated repository for development of the Python-based ITHUTIR Agent OS and Orchestrator.

## Purpose

Build a provider-independent agent operating system that converts goals into validated work while supporting the full Ithutir lifecycle:

`IDEA -> VALIDATION -> MONETIZATION MAP -> PLAN -> BUILD -> TEST -> PUBLISH -> DISTRIBUTE -> MONETIZE -> MEASURE -> IMPROVE`

The system is not tied to one LLM or executor.

Core principle:

`LLM Brain -> Python Orchestrator -> Executor -> Validation -> Feedback/Recovery`

Target executor classes:
- CLI executors such as Codex CLI / Gemini CLI;
- Computer Agent for Linux GUI/browser workflows;
- API/connectors where direct integrations are safer or more reliable.

## Repository boundary

This repository contains Agent OS / Orchestrator code and its governance/architecture.

The `merxdc12/ithutir` repository remains separate and contains the Ithutir website/business platform. ITHUTIR Agent OS may manage that repository as a project, but its own source code must remain here.

## Current development state

- Lab 01: local Python -> Codex CLI prototype already exists on the development PC and will be imported only after comparing local and remote state.
- Lab 01.5: Governance Foundation.
- Lab 02: Brain/Executor abstraction.
- Further implementation follows the master roadmap in `docs/ROADMAP.md`.

## Safety

Do not store API keys, tokens, passwords, runtime secrets, or credentials in Git.
Do not overwrite the existing local `~/ithutir-agent-os/` prototype during initial repository setup.
