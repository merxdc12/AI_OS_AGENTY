#!/usr/bin/env python3

import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime


def load_task(task_file: Path) -> dict:
    """Load task definition from JSON."""

    with task_file.open("r", encoding="utf-8") as file:
        return json.load(file)


def run_command(command: list[str], cwd: Path) -> subprocess.CompletedProcess:
    """Run local command without shell."""

    return subprocess.run(
        command,
        cwd=cwd,
        capture_output=True,
        text=True,
    )


def git_preflight(project_dir: Path) -> dict:
    """Check repository state before Codex is allowed to run."""

    repo_check = run_command(
        ["git", "rev-parse", "--is-inside-work-tree"],
        project_dir,
    )

    if repo_check.returncode != 0:
        return {
            "ok": False,
            "reason": "Project directory is not a Git repository.",
        }

    branch_result = run_command(
        ["git", "branch", "--show-current"],
        project_dir,
    )

    branch = branch_result.stdout.strip()

    status_result = run_command(
        ["git", "status", "--porcelain"],
        project_dir,
    )

    dirty = bool(status_result.stdout.strip())

    head_result = run_command(
        ["git", "log", "-1", "--oneline"],
        project_dir,
    )

    head = head_result.stdout.strip()

    if not branch:
        return {
            "ok": False,
            "reason": "Detached HEAD detected.",
            "branch": branch,
            "dirty": dirty,
            "head": head,
        }

    if branch in {"main", "master"}:
        return {
            "ok": False,
            "reason": f"Refusing to run Codex directly on protected branch: {branch}",
            "branch": branch,
            "dirty": dirty,
            "head": head,
        }

    if dirty:
        return {
            "ok": False,
            "reason": "Working tree is not clean before task execution.",
            "branch": branch,
            "dirty": dirty,
            "head": head,
        }

    return {
        "ok": True,
        "reason": "Preflight passed.",
        "branch": branch,
        "dirty": dirty,
        "head": head,
    }


def build_prompt(task: dict) -> str:
    """Convert structured task JSON into a prompt for Codex."""

    requirements = "\n".join(
        f"- {item}"
        for item in task.get("requirements", [])
    )

    verification = "\n".join(
        f"- {item}"
        for item in task.get("verification", [])
    )

    prompt = f"""
TASK ID:
{task["task_id"]}

GOAL:
{task["goal"]}

REQUIREMENTS:
{requirements}

VERIFICATION:
{verification}

IMPORTANT:
Work only inside the current repository.
Do not commit.
Do not push.
Do not change Git branches.

Return a concise technical summary containing:
- changed files
- tests executed
- test results
- any deviations from the requested scope
"""

    return prompt.strip()


def run_codex(prompt: str, project_dir: Path) -> dict:
    """Run Codex CLI inside the project directory."""

    try:
        result = subprocess.run(
            [
                "codex",
                "exec",
                prompt,
            ],
            cwd=project_dir,
            capture_output=True,
            text=True,
        )

    except FileNotFoundError:
        return {
            "status": "error",
            "exit_code": None,
            "stdout": "",
            "stderr": "Codex CLI not found.",
        }

    except Exception as error:
        return {
            "status": "error",
            "exit_code": None,
            "stdout": "",
            "stderr": str(error),
        }

    status = (
        "success"
        if result.returncode == 0
        else "failed"
    )

    return {
        "status": status,
        "exit_code": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


def save_result(
    task: dict,
    codex_result: dict,
    output_file: Path,
    preflight: dict,
) -> None:
    """Save execution result as JSON."""

    result = {
        "task_id": task["task_id"],
        "timestamp": datetime.now().isoformat(),
        "project_dir": task["project_dir"],
        "preflight": preflight,
        "status": codex_result["status"],
        "exit_code": codex_result["exit_code"],
        "stdout": codex_result["stdout"],
        "stderr": codex_result["stderr"],
    }

    with output_file.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            result,
            file,
            indent=4,
            ensure_ascii=False,
        )


def main():

    if len(sys.argv) != 2:

        print(
            "Usage:\n"
            "python3 orchestrator.py task.json"
        )

        sys.exit(1)

    task_file = Path(
        sys.argv[1]
    ).expanduser().resolve()

    if not task_file.exists():

        print(
            f"ERROR: Task file not found: "
            f"{task_file}"
        )

        sys.exit(1)

    task = load_task(task_file)

    project_dir = Path(
        task["project_dir"]
    ).expanduser().resolve()

    if not project_dir.exists():

        print(
            f"ERROR: Project directory "
            f"does not exist: {project_dir}"
        )

        sys.exit(1)

    print("=" * 64)
    print("ITHUTIR AGENT OS v0.0.3")
    print("=" * 64)

    print(f"\nTask ID : {task['task_id']}")
    print(f"Project : {project_dir}")

    print("\n[PRE-FLIGHT] Checking repository...")

    preflight = git_preflight(project_dir)

    print(f"Branch  : {preflight.get('branch', 'N/A')}")
    print(f"HEAD    : {preflight.get('head', 'N/A')}")
    print(f"Dirty   : {preflight.get('dirty', 'N/A')}")
    print(f"Result  : {preflight['reason']}")

    if not preflight["ok"]:

        print("\nABORTED.")
        print("Codex was NOT started.")

        sys.exit(2)

    prompt = build_prompt(task)

    print("\n[ORCHESTRATOR] Pre-flight passed.")
    print("[ORCHESTRATOR] Sending task to Codex...")

    codex_result = run_codex(
        prompt,
        project_dir,
    )

    output_file = Path(
        __file__
    ).resolve().parent / "result.json"

    save_result(
        task,
        codex_result,
        output_file,
        preflight,
    )

    print("\n" + "=" * 64)
    print("RESULT")
    print("=" * 64)

    print(f"Status      : {codex_result['status']}")
    print(f"Exit code   : {codex_result['exit_code']}")
    print(f"Result file : {output_file}")

    print("\n--- CODEX RESPONSE ---")
    print(codex_result["stdout"])

    if codex_result["stderr"]:

        print("\n--- CODEX LOG ---")
        print(codex_result["stderr"])


if __name__ == "__main__":
    main()