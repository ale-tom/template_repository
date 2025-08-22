from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


def _run(cmd: list[str], cwd: str | None = None) -> bool:
    """
    Run a command and return True on success. Errors are written to stderr and not raised.
    Useful for best-effort bootstrap steps where failure should not abort generation.
    """
    try:
        subprocess.run(cmd, check=True, cwd=cwd)
        return True
    except Exception as exc:  # noqa: BLE001
        sys.stderr.write(f"Warning: command failed: {cmd} -> {exc}\n")
        return False


def _has_exe(name: str) -> bool:
    """
    Return True if an executable is available on PATH. Used to gate optional steps like Poetry.
    """
    return shutil.which(name) is not None


def _ensure_vscode_settings(project_dir: Path) -> None:
    """
    Ensure a minimal VS Code settings file exists that points to the in-project virtualenv.
    """
    vscode = project_dir / ".vscode"
    vscode.mkdir(exist_ok=True)
    settings = {
        "python.defaultInterpreterPath": f"{project_dir}/.venv/bin/python",
        "python.testing.pytestEnabled": True,
        "python.testing.pytestArgs": ["tests"],
        "editor.formatOnSave": True,
    }
    (vscode / "settings.json").write_text(json.dumps(settings, indent=2))


def _write_poetry_toml(project_dir: Path) -> None:
    """
    Write poetry.toml to enforce in-project virtualenvs and prefer the active Python if present.
    If the file already exists, do nothing.
    """
    poetry_toml = project_dir / "poetry.toml"
    if poetry_toml.exists():
        return
    content = "[virtualenvs]\n" "in-project = true\n" "prefer-active-python = true\n"
    poetry_toml.write_text(content)


def _homebrew_python_for(version_mm: str) -> str | None:
    """
    Return a Homebrew Python executable path that matches major.minor, if installed.
    Checks Apple Silicon and Intel default locations.
    """
    parts = version_mm.split(".")
    if len(parts) < 2:
        return None
    major, minor = parts[0], parts[1]
    candidates = [
        f"/opt/homebrew/opt/python@{major}.{minor}/bin/python{major}.{minor}",  # Apple Silicon
        f"/usr/local/opt/python@{major}.{minor}/bin/python{major}.{minor}",  # Intel macOS
    ]
    for c in candidates:
        p = Path(c)
        if p.exists() and os.access(p, os.X_OK):
            return c
    return None


def _choose_python(version_spec: str) -> str | None:
    """
    Choose a Python interpreter for Poetry to use.

    Preference order:
    1) Homebrew interpreter matching the requested major.minor (if present).
    2) The current interpreter (sys.executable) if it satisfies the requested version.
    3) Common executable names on PATH: pythonX.Y, python3, python.

    Returns the chosen executable path/name, or None if nothing suitable is found.
    """
    requested = version_spec.lstrip(">=").strip()  # e.g. "3.12"
    hb = _homebrew_python_for(requested)
    if hb:
        return hb

    # Try current Python if it meets the requested version.
    try:
        out = subprocess.check_output(
            [
                sys.executable,
                "-c",
                "import sys; print(f'{sys.version_info[0]}.{sys.version_info[1]}')",
            ]
        )
        current_mm = out.decode().strip()
        if current_mm >= requested:
            return sys.executable
    except Exception:  # noqa: BLE001
        pass

    # Fall back to common names.
    for name in (f"python{requested}", "python3", "python"):
        if shutil.which(name):
            return name

    return None


def _write_python_version_file(project_dir: Path, version_spec: str) -> None:
    """
    Write a .python-version file with the requested major.minor for pyenv/asdf users.
    """
    requested = version_spec.lstrip(">=").strip()
    (project_dir / ".python-version").write_text(f"{requested}\n")


def main() -> None:
    """
    Post-generation bootstrap for a VS Code + Poetry workflow.
    - Ensures .vscode settings and poetry.toml are present.
    - Selects a suitable Python interpreter (prefers Homebrew matching the requested version).
    - Creates an in-project .venv and installs dependencies including the 'dev' group.
    - Initializes a git repository and makes the initial commit.
    """
    project_dir = Path(".").resolve()

    if not (project_dir / ".vscode" / "settings.json").exists():
        _ensure_vscode_settings(project_dir)

    _write_poetry_toml(project_dir)
    _write_python_version_file(project_dir, "{{ cookiecutter.python_version }}")

    if _has_exe("poetry"):
        chosen = _choose_python("{{ cookiecutter.python_version }}")
        if chosen:
            _run(["poetry", "env", "use", chosen], cwd=str(project_dir))
        else:
            sys.stderr.write(
                "Warning: No suitable Python interpreter found; Poetry will attempt defaults. "
                "Consider installing the requested version via Homebrew or pyenv.\n"
            )

        # Install with dev group so tools (pytest, ruff, black, mypy) land in .venv/bin/
        # If you use optional-dependencies instead of Poetry groups, switch to: ["poetry", "install", "--extras", "dev"]
        _run(["poetry", "install", "--with", "dev"], cwd=str(project_dir))
    else:
        sys.stderr.write(
            "Info: Poetry not found on PATH; skipping dependency install.\n"
        )

    if _run(["git", "init", "-b", "main"], cwd=str(project_dir)):
        _run(["git", "add", "."], cwd=str(project_dir))
        _run(["git", "commit", "-m", "Initial commit"], cwd=str(project_dir))
    else:
        sys.stderr.write("Warning: git initialization skipped.\n")

    print(
        "\n✅ Project ready for VS Code. The .venv is in-project and dev tools are installed."
    )
    print(
        "Open the folder in VS Code; it should auto-detect the interpreter at .venv/bin/python."
    )
    print(
        "Useful commands: 'poetry shell', 'poetry run pytest -q', or Make targets like 'make test'."
    )


if __name__ == "__main__":
    main()
