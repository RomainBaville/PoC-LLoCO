# Optimization Playground (PoC)

This project is a **proof of concept (PoC)** for a generic optimization playground.
It provides a **guided, UI‑driven workflow** to help users:

1. Describe an optimization problem in natural language (must be updated)
2. Configure the problem step by step
3. Select an appropriate solver
4. Solve the problem
5. Receive an **AI‑generated explanation and summary** of the results (must be updated)

The long‑term goal is to build a **solver‑agnostic and problem‑agnostic platform** for constraint optimization.

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
- **Generic Assignment Problem** (bipartite assignment with requirements and constraints)

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
├── data/
│   └── ...
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
│       ├── matching/
│       │   └── ui_matching.py
│       │
│       ├── ressoucres/
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
│       ├── ressoucres/
│       │   └── ressoucre_config.py
│       │
│       └── matching/
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
│           │   └── generic_constraints.py
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
└── requirements.txt
```

---

## Running the Application

This project has been developed and tested on **Windows**.

To run the application, follow these steps:

1. **Prepare the data**
   - Place your input files in the `data/` directory
   - Only **CSV files** are supported for now

2. **Prepare the LLM model**
   - Place a `.gguf` **Qwen model** in the `models/` directory
   - Models can be downloaded from: https://huggingface.co/Qwen

3. **Prepare llama.cpp**
   - Place the `llama.cpp` binaries and required files in the `llama_cpp/` directory
   - Precompiled releases are available here: https://github.com/ggml-org/llama.cpp/releases

4. **Run the application**
   - Execute `run_app.bat` from a terminal

   This will:
   - Open **two terminal windows**:
     - one running the **llama.cpp server**
     - one running the **Streamlit application**
   - Automatically open the application in your web browser

5. **Shut down**
   - Close the browser window when finished
   - Press **`e`** in the terminal used to execute the bat file to terminate all running processes

### Notes
- The LLM is used only for **onboarding guidance** and **solution summarization**
- All optimization computations are performed by deterministic solvers
- Once the models are downloaded, **no internet connection is required**
