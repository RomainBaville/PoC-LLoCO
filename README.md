
# Optimization Playground (PoC)

## Overview

This project is a **Proof of Concept (PoC)** for a generic optimization playground.

It aims to provide a **guided, UI‑driven workflow** to help users:

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
  - Auto fill the interface
  - guides the user through the modeling process

This lowers the entry barrier for non-experts.
Note that the user can user the program whitout using any AI.

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

- **Launcher**: launch the ui app and any terminal depending of the os
- **UI defines semantics**: labels, data mapping, user meaning
- **Domain defines structure**: mathematical modeling
- **Solvers define math**: constraints and optimization engines
- **Registries declare capabilities**: problems and solvers
- **LLM assists but never replaces solvers**

Benefits:

- Add new solvers without changing UI
- Add new domain without changing solvers
- Adapte the interface depending of domain and solver
- Keep AI decoupled from optimization logic

---

## Project Structure

```
PoC-LLoCO/
│
├── models/
│   └── ...
│
├── llama_cpp/
│   └── ...
│
├── domain/
│   ├── assignment/
│   │   │
│   │   ├── constraints/
│   │   │   ├── constraints_config.py
│   │   │   ├── logicals_constraints.py
│   │   │   └── quantities_constraints.py
│   │   │
│   │   ├── score/
│   │   │   ├── matching_config.py
│   │   │   ├── matching_penalty_functions.py
│   │   │   ├── matching_reward_functions.py
│   │   │   ├── ressources_config.py
│   │   │   └── score_config.py
│   │   │
│   │   └── base.py
│   │
│   ├── objective.py
│   └── registry.py
│
├── infrastructure/
│   ├── csv_loader.py
│   └── registry.py
│
├── launcher/
│   ├── run_app.py
│   └── utils.py
│
├── llm/
│   ├── client/
│   │   ├── akkodis_client.py
│   │   ├── llama_client.py
│   │   └── registry.py
│   │
│   ├── onboarding/
│   │   ├── onboarding_context.py
│   │   ├── onboarding_prompt.py
│   │   └── utils.py
│   │
│   ├── summary/
│   │   ├── summary_context.py
│   │   ├── summary_prompt.py
│   │   └── utils.py
│   │
│   └── utils.py
│
├── solvers/
│   ├── assignment/
│   │   ├── cp_model/
│   │   │   ├── constraints/
│   │   │   │   ├── logical_constraints.py
│   │   │   │   ├── matching_constraints.py
│   │   │   │   ├── quantities_constraints.py
│   │   │   │   ├── ressources_constraints.py
│   │   │   │   └── solver_constraints.py
│   │   │   │
│   │   │   └── ortools_cp_sat.py
│   │   │
│   │   └── registry.py
│   │
│   └── registry.py
│
├── tests/
│   ├── assignment/
│   │   ├── problem_i/                       # Folder with data for the assignment problem i from the json file
│   │   │   ├── problem_i_description.py     # Build the AssignmentProblem with the solution
│   │   │   ├── left_data_i.csv              # The csv file with the left data for the ui
│   │   │   └── right_data_i.csv             # The csv file with the right data for the ui
:   :   :
│   │   │
│   │   └── test_assignments_problem.py      # The file with all the tests for assignments problem
│   │
│   └── IndustryOR.json                      # All the problem the project needs to solve at the end
│
├── ui/
│   ├── assignment/
│   │   ├── constraints/
│   │   │   ├── builder.py
│   │   │   ├── ui_logicals_constraints.py
│   │   │   └── ui_quantities_constraints.py
│   │   │
│   │   ├── score/
│   │   │   ├── builder.py
│   │   │   ├── ui_matching.py
│   │   │   └── ui_ressources.py
│   │   │
│   │   ├── builder.py
│   │   ├── ui_assignment.py
│   │   └── ui_data_sources.py
│   │
│   ├── app.py
│   ├── registry.py
│   ├── sidebar.py
│   ├── theme.py
│   └── utils.py
│
├── .pre-commit-config.yaml
├── LICENSE
├── pyproject.toml
├── README.md
└── uv.lock
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

## Running the Application

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

The application opens automatically at **http://localhost:8501**.

#### Windows

```bash
# activate venv first
.venv\Scripts\activate

# launch Streamlit
python launcher\run_app.py
```

#### macOS

```bash
# activate venv first
source .venv/bin/activate

# launch Streamlit
python launcher/run_app.py
```

#### Linux

```bash
# activate venv first
source .venv/bin/activate

# launch Streamlit
python launcher/run_app.py
```

This will:

- Open a new terminal to start Streamlit UI
- Open the app in your browser

---

### 5. Shutdown

- Close the window on your browser
- Press `Q` in the first terminal

---

## Code Quality & Tooling

### Testing

Tests are implemented to check solvers. To run all tests:

```bash
uv run pytest
```

---

### LLM Backend (optional)

The LLM is used for two optional features: problem onboarding guidance and solution summarization.
**The optimizer works fully without a LLM** — simply leave the model selector set to "Chose your AI model".

Two backends are supported and auto-detected by the application:

#### Option A — AKKODIS Azure OpenAI (recommended for AKKODIS employees)

The application automatically discovers AKKODIS GPT models when an API key is present.
Available models: `GPT-4o mini`, `GPT-4o`, `GPT-5`, `o4-mini`.

Place your API key in **the root directory** and name it **akkodis_openAI_api_key.txt**

> **Security:** `akkodis_openAI_api_key.txt` is listed in `.gitignore` and must **never** be committed.

No server to start — models appear automatically in the picker when the key is found.

#### Option B — llama-server + GGUF (local)

1. Download a Qwen GGUF model from https://huggingface.co/Qwen and place it in `models/`
2. Download llama.cpp binaries from https://github.com/ggml-org/llama.cpp/releases and place them in `llama_cpp/`

Notes:
  - Splited models with several gguf files (00001-of-*) are automaticly detected, do not change names.
  - The llama server is open on a new terminal if a Qwen model is selected and close at the automaticly.

---

### Using the Application

1. **Sidebar** — configure your problem step by step:
   - Select a problem type and formulation
   - Choose your CSV files and map the columns
   - Select a solver
   - *(Optional)* Select a local LLM model for AI features
2. Click **▶ Résoudre** to run the optimizer
3. **Results** appear in the main area: metrics, assignment table, AI summary, and ZIP export

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

- push (on the main branch)
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
uv sync --extra dev --frozen
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
uv run yapf -r -i domain solvers infrastructure ui tests llm launcher
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
