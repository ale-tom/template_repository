# {{ cookiecutter.project_name }}
Some text

[![Build Status](https://github.com/ale-tom/linkedin-job-analysis/actions/workflows/ci.yml/badge.svg)](https://github.com/ale-tom/linkedin-job-analysis/actions)
[![Coverage Status](https://coveralls.io/repos/github/ale-tom/linkedin-job-analysis/badge.svg?branch=master)](https://coveralls.io/github/ale-tom/linkedin-job-analysis?branch=master)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org)
[![Repo Size](https://img.shields.io/github/repo-size/ale-tom/linkedin-job-analysis)](https://github.com/ale-tom/linkedin-job-analysis)

## Overview

{{ cookiecutter.description }}


Author: {{ cookiecutter.author_name }} <{{ cookiecutter.author_email }}>

## Repository structure
```
{{ cookiecutter.project_name }}/
├── data/               # Raw and processed data files
├── docs/               # Documentation 
├── notebooks/          # Jupyter notebooks s
│   └── analysis.ipynb
├── src/                # Source code
│   └── __init__.py
├── tests/              # Unit tests (using pytest)
│   └── test_smoke.py
├── .github/            # GitHub configuration files 
│   ├── workflows/
│   │   └── ci.yml      # Continuous Integration (CI) configuration using GitHub Actions
│   └── ISSUE_TEMPLATE.md
├── LICENSE             # License file 
├── README.md           # Project overview, badges, setup instructions, etc.
└── pyproject.toml      # Packaging configuration
```

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/ale-tom/{{ cookiecutter.project_name }}.git
   cd {{ cookiecutter.project_name }}
   ```

2. Quickstart
```poetry install
   poetry shell
   pytest -q
```
## Usage
```
```

## Licence

MIT License

Copyright (c) {{ cookiecutter.author_name }}