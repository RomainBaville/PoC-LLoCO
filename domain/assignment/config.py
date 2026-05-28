# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from dataclasses import dataclass
from typing import Optional, Dict, List, Tuple


@dataclass
class AssignmentModelConfig:
    # -----------------------------
    # Structure
    # -----------------------------
    max_assignments_per_left: int = 1
    max_assignments_per_right: Optional[int] = None
    force_all_left_assigned: bool = False
    min_assignments_per_right: Optional[int] = None

    # -----------------------------
    # Objective
    # -----------------------------
    reward_mode: str = "min"
    penalty_mode: Optional[str] = None
    penalty_weight: float = 1.0
    skill_weights: Optional[Dict[str, float]] = None

    # -----------------------------
    # Advanced
    # -----------------------------
    use_demand_penalty: bool = False
    demand_weight: float = 1.0

    forbidden_pairs: Optional[List[Tuple[str, str]]] = None
    balance_weight: float = 0.0

    # -----------------------------
    # Coverage behavior
    # -----------------------------
    enforce_full_coverage: bool = False
