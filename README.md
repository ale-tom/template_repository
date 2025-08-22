# Python Project Template with Cookiecutter & Poetry

A modern, opinionated Python project template for **data science** and **software engineering** workflows.  
One command creates a fully tooled-up project with:

- **Poetry** for dependency management & virtual environments  
- **Cookiecutter** for project scaffolding  
- **Pre-configured VS Code settings** with automatic interpreter detection  
- **Makefile shortcuts** for install, test, format  
- **Testing, linting, formatting** via `pytest`, `ruff`, `black`, `mypy`  
- **GitHub Actions CI** for automated testing  
- **Reproducible environments** and clean project structure  

---

## 🚀 Quick Start

### 1. Install tools

We recommend using `pipx` so your global Python stays clean:

```bash
pipx install cookiecutter
pipx install poetry
```

### 2. Generate a new project

```bash
cookiecutter https://github.com/ale-tom/template_repository.git
```
You’ll be prompted for:
Project name
Python version
Author details
Licence choice
Cookiecutter will create the project, set up `.venv`, install dependencies, and initialise Git.

## 📂 Project Structure
Generated projects look like this:
```bash
my_project/
├── pyproject.toml          # Poetry + project metadata
├── poetry.toml             # Poetry settings (in-project .venv)
├── Makefile                # Install, test, format shortcuts
├── README.md
├── LICENSE
├── src/my_project/         # Your Python package
│   └── __init__.py
├── tests/                  # Pytest tests
│   └── test_smoke.py
├── .vscode/                # VS Code config
│   └── settings.json
└── .github/workflows/ci.yml  # GitHub Actions CI
```

## 🛠 Common Commands
Inside the new project folder:

```bash
# Install dependencies (incl. dev tools)
poetry install --with dev

# Activate virtual environment
poetry shell

# Run tests
make test

# Format code
make format

# Lint code
poetry run ruff check src
```

VS Code automatically detects `.venv` for linting, testing, and debugging.

## 🧪 GitHub Actions CI

The generated project includes a basic CI pipeline:
Runs on each push
Installs dependencies
Runs tests and lint checks
Ready to integrate with GitHub from day one.

## 🧩 Why this template?

* Consistency: Same structure & tools across all projects
* Speed: One command → ready-to-code environment
* Reproducibility: Poetry lockfile ensures identical environments
* Best practices: Testing, linting, formatting, CI included out of the box
