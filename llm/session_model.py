# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class OptimizationSession:
    """
    Structured representation of a complete optimization run.
    Passed to the LLM prompt builder.
    """

    # High-level structure
    problem_family: str           # e.g. "Assignment"
    problem_type: str             # e.g. "Skill-based assignment"
    problem_variant: str          # e.g. "Coverage"

    # Workflow trace
    steps: List[str]

    # Data
    data_description: str

    # Solver
    solver_name: str

    # Result
    result_summary: str

    # Optional
    solver_family: Optional[str] = None
    solver_description: Optional[str] = None
    result_details: Dict[str, str] = field(default_factory=dict)
