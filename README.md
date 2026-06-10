# Optimization Playground (PoC)

This project is a **proof of concept (PoC)** for a generic optimization playground.
It provides a **guided, UI‑driven workflow** to help users:

1. Describe an optimization problem in natural language
2. Configure the problem step by step
3. Select an appropriate solver
4. Solve the problem
5. Receive an **AI‑generated explanation and summary** of the results

The long‑term goal is to build a **solver‑agnostic and problem‑agnostic platform**
for constraint optimization.

---

## Role of the LLM (AI Assistant)

The project integrates a Large Language Model (LLM) at **two key points** of the user journey:

### 1. Problem onboarding (start of the flow)
At the beginning of the application, the user can describe their problem in plain language.
The LLM is used to:
- explain how the tool can help
- clarify what type of optimization problem the user is facing
- guide the user into the appropriate modeling flow

This lowers the entry barrier for non‑experts in optimization.

### 2. Solution summarization (end of the flow)
After the solver produces a solution, the LLM is used to:
- summarize the assignment / optimization result in natural language
- explain the outcome using the user’s own terminology
- provide a human‑readable interpretation of the solution

The LLM **never replaces the solver**: it acts as a **guidance and explanation layer** only.

---

## Features

- Streamlit-based interactive UI — single-page dashboard layout
- Sidebar-driven configuration with progressive disclosure
- Multi-backend LLM model picker: Ollama, llama-server, and AKKODIS Azure OpenAI (auto-detected)
- LLM-assisted onboarding and result summarization
- Generic domain modeling (solver-agnostic)
- Registry-based problem and solver selection
- Support for multiple solvers per problem
- Clean object-oriented architecture

Currently implemented:
- **Generic Assignment Problem** (bipartite assignment with requirements)
  - Skill coverage · Best-fit matching · Team formation · Portfolio selection

---

## Architectural Principles

- **UI defines semantics**
  (labels, CSV mappings, user meaning)
- **Domain defines structure**
  (mathematical representation)
- **Solvers define math**
  (constraints, objectives, optimization engines)
- **Registries declare capabilities**
  (available problems and solvers)
- **LLM assists the user**, but does not solve problems

This separation allows:
- adding new solvers without touching the UI
- adding new problems without changing solver code
- integrating AI safely without coupling it to optimization logic

---

## Project Structure
```
PoC-LLoCO/
│
├── README.md
│
├── data/                             # Input datasets (CSV for now)
│   └── ...
│
├── models/                           # Local LLM models (GGUF)
│   └── ...
│
├── llama_cpp/                        # llama.cpp runtime & binaries
│   └── ...
│
├── ui/                               # Streamlit UI layer
│   ├── app.py                        # Main entry point — dashboard orchestrator
│   ├── registry.py                   # Problem FAMILY registry (Assignment, etc.)
│   ├── sidebar.py                    # Sidebar — progressive configuration panel
│   ├── theme.py                      # CSS design system and render helpers
│   ├── model_picker.py               # LLM model discovery (Ollama, llama-server, AKKODIS)
│   ├── akkodis_client.py             # AKKODIS Azure OpenAI client (mirrors LLoCO/llm_utils.py)
│   ├── utils.py                      # Journey logging, AI summary, ZIP export
│   │
│   └── problems/
│       ├── assignment/               # Assignment problem family
│       │   ├── registry.py           # Assignment TYPES registry (skills, cost, …)
│       │   │
│       │   └── skills/               # Skill-based assignment TYPE
│       │       ├── registry.py       # Skill VARIANTS registry (coverage, best_fit…)
│       │       ├── builder.py        # Generic skills builder (registry-driven)
│       │       ├── ui_coverage.py    # Coverage variant — render_results
│       │       ├── ui_best_fit.py    # Best-fit variant — render_results
│       │       ├── ui_team.py        # Team variant — render_results
│       │       └── ui_portfolio.py   # Portfolio variant — render_results
│       │
│       └── base.py                   # Base UI contracts
│
├── domain/                           # Solver-agnostic mathematical models
│   ├── base.py                       # Base DomainProblem
│   ├── entity_registry.py            # Entity identity & uniqueness handling
│   │
│   └── assignment/                   # Assignment family (math side)
│       ├── base.py                   # AssignmentBaseProblem
│       │
│       └── skills/                   # Skill-based assignment models
│           ├── base.py               # SkillAssignmentProblem (dataclass!)
│           ├── coverage.py           # SkillCoverageAssignment
│           ├── best_fit.py           # SkillBestFitAssignment
│           ├── team.py               # SkillTeamAssignment
│           └── portfolio.py          # SkillPortfolioSelection
│
├── solvers/                          # Solver layer (execution)
│   ├── base.py                       # Solver interface
│   │
│   └── assignment/                   # Assignment solvers
│       ├── registry.py               # Assignment solver GROUPS (skills, cost…)
│       │
│       └── skills/                   # Skill-based solvers
│           ├── registry.py           # Skill solver registry (OR-Tools, etc.)
│           └── ortools_cp_sat.py     # OR-Tools CP-SAT solver (variant-aware)
│
├── infrastructure/                   # Data access layer
│   ├── base_loader.py                # Abstract data loader
│   ├── csv_loader.py                 # CSV loader
│   └── registry.py                   # Data source registry
│
├── llm/                              # LLM integration layer
│   ├── client.py                     # LLM client (llama.cpp)
│   ├── session_model.py              # OptimizationSession dataclass
│   ├── session_prompt.py             # Solver-aware summary prompt
│   ├── onboarding_context.py         # Registry-driven onboarding context
│   └── onboarding_prompt.py          # Onboarding prompt builder
│
└── requirements.txt                  # Python dependencies
```

---

## Running the Application

### Prerequisites (all platforms)

- **Python 3.10+**
- CSV input files placed in the `data/` directory

Install Python dependencies (do this once, inside a virtual environment):

```bash
python -m venv .venv
```

| Platform | Activate venv | Install deps |
|----------|---------------|--------------|
| Windows  | `.venv\Scripts\activate` | `pip install -r requirements.txt` |
| macOS / Linux | `source .venv/bin/activate` | `pip install -r requirements.txt` |

---

### LLM Backend (optional)

The LLM is used for two optional features: problem onboarding guidance and solution summarization.
**The optimizer works fully without a LLM** — simply leave the model selector set to "Aucun".

Three backends are supported and auto-detected by the application:

#### Option A — AKKODIS Azure OpenAI (recommended for AKKODIS employees)

The application automatically discovers AKKODIS GPT models when an API key is present.
Available models: `GPT-4o mini`, `GPT-4o`, `GPT-5`, `o4-mini`.

Place your API key in **one** of the following locations (checked in order):

| Location | Notes |
|----------|-------|
| `OPENAI_API_KEY` environment variable | Highest priority |
| `.api_key.txt` at the project root | Local override |
| `../LLoCO/.api_key.txt` | Auto-detected from sibling project |

> **Security:** `.api_key.txt` is listed in `.gitignore` and must **never** be committed.

No server to start — models appear automatically in the picker when the key is found.

#### Option B — Ollama (recommended for local use, all platforms)

1. Install Ollama: https://ollama.com/download
2. Pull a model:
   ```bash
   ollama pull qwen3:0.6b   # lightweight (~522 MB, works on 8 GB RAM)
   # or
   ollama pull qwen3:8b
   ```
3. Ollama starts automatically at boot. If not running, start it:

   | Platform | Command |
   |----------|---------|
   | Windows  | Launch the **Ollama** desktop app |
   | macOS    | `ollama serve` or launch the **Ollama** menu-bar app |
   | Linux    | `ollama serve` |

   The application detects available models automatically — no configuration needed.

#### Option C — llama-server + GGUF (Windows, original setup)

1. Download a Qwen GGUF model from https://huggingface.co/Qwen and place it in `models/`
2. Download llama.cpp binaries from https://github.com/ggml-org/llama.cpp/releases and place them in `llama_cpp/`
3. Start the server manually before launching the app:
   ```bat
   llama_cpp\llama-server.exe -m models\<model-name>.gguf --port 8080
   ```

---

### Launching the UI

#### Windows

```bat
REM activate venv first
.venv\Scripts\activate

REM launch Streamlit
streamlit run ui\app.py
```

Or use the provided script which also starts llama-server (Option C only):
```bat
run_app.bat
```

#### macOS

```bash
# activate venv first
source .venv/bin/activate

# launch Streamlit
streamlit run ui/app.py
```

#### Linux

```bash
# activate venv first
source .venv/bin/activate

# launch Streamlit
streamlit run ui/app.py
```

The application opens automatically at **http://localhost:8501**.
To use a different port: `streamlit run ui/app.py --server.port 8502`

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

### Notes

- All optimization computations are performed by **deterministic solvers** — the LLM never affects the result
- The model picker auto-detects all three backends (AKKODIS, Ollama, llama-server) at each page load
- AKKODIS GPT models require an internet connection; Ollama and llama-server run fully offline
- `.api_key.txt` is gitignored — never commit it