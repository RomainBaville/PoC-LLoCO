# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class OptimizationSession:
    """
    Structured record of an optimization run.
    This is the ONLY object given to the LLM prompt builder.
    """

    # High-level
    problem_family: str                # e.g. "assignment"
    problem_variant: str               # e.g. "skill-based assignment"

    # User path
    steps: List[str]                   # ordered, human-readable steps

    # Data
    data_description: str              # what data the user provided

    # Solver
    solver_name: str                   # e.g. "OR-Tools CP-SAT"
    result_summary: str                # compact textual result
    solver_type: Optional[str] = None  # e.g. "constraint programming"

    # Results
    result_details: Optional[Dict[str, Any]] = field(default_factory=dict)
