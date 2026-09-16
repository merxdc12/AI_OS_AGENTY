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

Return a concise technical summary of the result.
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
) -> None:
    """Save execution result as JSON."""

    result = {
        "task_id": task["task_id"],
        "timestamp": datetime.now().isoformat(),
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

    prompt = build_prompt(task)

    print("=" * 60)
    print("ITHUTIR AGENT OS v0.0.2")
    print("=" * 60)

    print(
        f"\nTask ID: "
        f"{task['task_id']}"
    )

    print(
        f"Project: "
        f"{project_dir}"
    )

    print(
        "\n[ORCHESTRATOR] "
        "Sending task to Codex..."
    )

    codex_result = run_codex(
        prompt,
        project_dir,
    )

    output_file = Path(
        "result.json"
    ).resolve()

    save_result(
        task,
        codex_result,
        output_file,
    )

    print("\n" + "=" * 60)
    print("RESULT")
    print("=" * 60)

    print(
        f"Status: "
        f"{codex_result['status']}"
    )

    print(
        f"Exit code: "
        f"{codex_result['exit_code']}"
    )

    print(
        f"Result file: "
        f"{output_file}"
    )

    print("\n--- CODEX RESPONSE ---")

    print(
        codex_result["stdout"]
    )

    if codex_result["stderr"]:

        print(
            "\n--- CODEX LOG ---"
        )

        print(
            codex_result["stderr"]
        )


if __name__ == "__main__":
    main()
