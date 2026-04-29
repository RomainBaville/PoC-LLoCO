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

- Streamlit-based interactive UI
- Wizard-style problem configuration
- LLM-assisted onboarding and result explanation
- Generic domain modeling (solver-agnostic)
- Registry-based problem and solver selection
- Support for multiple solvers per problem
- Clean object-oriented architecture

Currently implemented:
- **Generic Assignment Problem** (bipartite assignment with requirements)

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
PoC-LLoCO/
│
├── README.md
├── data/                        # Folder with the data to use to solve the problem
│   └── ...
│
├── ui/
│   ├── app.py                   # Main Streamlit entry point
│   ├── registry.py              # Problem registry
│   ├── utils.py                 # Navigation & shared UI helpers
│   │
│   └── problems/
│       ├── assignment_ui.py     # Assignment problem wizard
│       ├── base.py              # (Optional) base UI contract
│       └── __init__.py
│
├── domain/
│   ├── assignment_structure.py  # Generic assignment structure
│   └── __init__.py
│
├── solvers/
│   ├── base.py                  # Solver interface
│   ├── assignment_ortools.py    # OR-Tools CP-SAT solver
│   ├── registry.py              # Solver registry per problem
│   └── __init__.py
│
├── infrastructure/
│   ├── base_loader.py
│   ├── csv_loader.py         # generic CSV loader
│   └── __init__.py
│
├── llm/
│   ├── client.py                # LLM API client
│   ├── summary.py               # Prompt builders (onboarding & summary)
│   └── __init__.py
│
└── requirements.txt