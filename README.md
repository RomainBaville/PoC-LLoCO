
# Optimization Playground (PoC)

## Overview

This project is a **Proof of Concept (PoC)** for a generic optimization playground.

It provides a **guided, UI‑driven workflow** to help users:

1. Describe an optimization problem (LLM-assisted)
2. Configure the problem step by step
3. Select an appropriate solver
4. Solve the problem
5. Receive an **AI-generated explanation of the results**

The long-term goal is to build a **solver-agnostic and problem-agnostic platform** for constraint optimization.

---

## Role of the LLM (AI Assistant)

The LLM is used strictly as a **guidance and explanation layer**.

### 1. Problem onboarding

At the beginning:

- The user describes their problem in natural language
- The LLM:
  - clarifies the problem type
  - explains how the tool can help
  - guides the user through the modeling process

This lowers the entry barrier for non-experts.

---

### 2. Solution explanation

After solving:

- The LLM generates:
  - a natural language explanation
  - a summary aligned with the user’s terminology

Important:
The LLM **does NOT perform optimization**.
All computations are done by deterministic solvers.

---

## Architectural Principles

- **UI defines semantics** → labels, CSV mapping, user meaning
- **Domain defines structure** → mathematical modeling
- **Solvers define math** → constraints and optimization engines
- **Registries declare capabilities** → problems and solvers
- **LLM assists but never replaces solvers**

Benefits:

- Add new solvers without changing UI
- Add new problems without changing solvers
- Keep AI decoupled from optimization logic

---

## Project Structure

```
PoC-LLoCO/
│
├── tests/
│   ├── IndustryOR.json          # All the problem the project needs to solve at the end
│   │
│   └── assignment/
│       ├── problem_i/           # Folder with data for problem from the json file
│       │   ├── problem_i.py     # Build the AssignmentProblem and the solution
│       │   ├── left_data_i.csv
│       │   └── right_data_i.csv
:       :
│       │
│       └── test_assignments_problem.py
│
├── models/
│   └── ...
│
├── llama_cpp/
│   └── ...
│
├── ui/
│   ├── app.py
│   ├── registry.py
│   ├── utils.py
│   │
│   └── assignment/
│       ├── constraints/
│       │   ├── builder.py
│       │   ├── ui_logicals_constraints.py
│       │   └── ui_quantities_constraints.py
│       │
│       ├── score/
│       │   ├── builder.py
│       │   ├── ui_matching.py
│       │   └── ui_ressources.py
│       │
│       ├── builder.py
│       └── ui_assignment.py
│
├── domain/
│   ├── objective.py
│   │
│   └── assignment/
│       ├── base.py
│       │
│       ├── constraints/
│       │   ├── constraints_config.py
│       │   ├── logicals_constraints.py
│       │   └── quantities_constraints.py
│       │
│       └── score/
│           ├── score_config.py
│           ├── ressources_config.py
│           ├── matching_config.py
│           ├── matching_penalty_functions.py
│           └── matching_reward_functions.py
│
├── solvers/
│   ├── base.py
│   ├── registry.py
│   │
│   └── assignment/
│       ├── registry.py
│       │
│       └── cp_model/
│           ├── constraints/
│           │   └── quantities_constraints.py
│           │   └── logical_constraints.py
│           │   └── matching_constraints.py
│           │   └── ressources_constraints.py
│           │
│           └── ortools_cp_sat.py
│
├── infrastructure/
│   ├── base_loader.py
│   ├── csv_loader.py
│   └── registry.py
│
├── llm/
│   ├── client.py
│   ├── session_model.py
│   ├── session_prompt.py
│   ├── onboarding_context.py
│   └── onboarding_prompt.py
│
├── .pre-commit-config.yaml
├── project.toml
├── uv.lock
│
├── README.md
└── run_app.bat
```


---

## Requirements

- Python == 3.12
- https://github.com/astral-sh/uv

---

## Installation (Reproducible Environment)

```bash
uv sync --extra dev --frozen
```

Uses `uv.lock`
Guarantees identical environments for all developers and CI

---

## ▶Running the Application

### 1. Prepare data

- Only CSV format is supported for now

---

### 2. Prepare LLM model

- Place a `.gguf` Qwen model in `models/`
- Download:
  https://huggingface.co/Qwen

---

### 3. Prepare llama.cpp

- Place binaries in `llama_cpp/`
- Download:
  https://github.com/ggml-org/llama.cpp/releases

---

### 4. Run application

```bash
run_app.bat
```

This will:

- Start `llama.cpp` server
- Start Streamlit UI
- Open the app in your browser

---

### 5. Shutdown

- Close the browser
- Press `Q` in the terminal

---

## Testing

Run all tests:

```bash
uv run pytest
```

---

## Code Quality & Tooling

The project enforces strict quality standards:

| Tool       | Purpose                  |
|------------|--------------------------|
| Ruff       | Linting                  |
| MyPy       | Static typing (strict)   |
| Yapf       | Formatting (custom)      |
| Pytest     | Testing                  |
| Pre-commit | Local validation         |

---

## Lint

```bash
uv run ruff check .
```

---

## Typing

```bash
uv run mypy .
```

---

## Formatting

```bash
uv run yapf -r -i .
```

---

## Code Style

This project uses a **custom readable style**:

```python
tuple[ str, ... ]
( left_label, matching_label )
```

This is intentional
Do NOT use:

- `black`
- `ruff format`

Formatting is handled by **yapf only**.

---

## Pre-commit Hooks (REQUIRED)

### Install:

```bash
uv run pre-commit install
```

### Run manually:

```bash
uv run pre-commit run --all-files
```

### Checks performed:

- Ruff (lint)
- MyPy (types)
- Yapf (format)

---

## Continuous Integration

CI runs automatically on:

- push
- pull requests

It verifies:

- lint
- typing
- tests

---

## Reproducible Environment

This project relies on:

```
pyproject.toml
uv.lock
```

### Rules

Always commit:

```
pyproject.toml
uv.lock
```

Always install with:

```bash
uv sync --frozen
```

Do NOT run install without `--frozen`

---

## Development Guidelines

### Always

- Add type annotations
- Write docstrings (Google style)
- Keep functions small and readable
- Respect architecture boundaries

---

### Avoid

- Editing `models/` and `llama_cpp`
- Untyped functions
- Dead code
- Using unauthorized formatters

---

## Quick Start

```bash
uv sync --extra dev --frozen

uv run pytest
uv run yapf -r -i domain solvers infrastructure ui tests
uv run ruff check .
uv run mypy .

uv run pre-commit run --all-files
```

---

## Contributing

1. Install environment
2. Enable pre-commit
3. Run all checks
4. Submit a Pull Request

---

## License

Apache-2.0
