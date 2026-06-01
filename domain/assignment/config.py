# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from dataclasses import dataclass
from typing import Optional, Dict, List, Tuple


@dataclass
class AssignmentModelConfig:
    # -----------------------------
    # STRUCTURE
    # -----------------------------
    max_assignments_per_left: int = 1
    max_assignments_per_right: Optional[int] = None
    min_assignments_per_right: Optional[int] = None
    force_all_left_assigned: bool = False

    # -----------------------------
    # OBJECTIVE
    # -----------------------------
    objective: str = "maximize"

    reward_mode: str = "min"
    penalty_mode: Optional[str] = None
    penalty_weight: float = 1.0
    skill_weights: Optional[Dict[str, float]] = None

    # -----------------------------
    # SCORING EXTENSIONS
    # -----------------------------
    use_cost: bool = False
    use_preferences: bool = False

    cost_weight: float = 1.0
    preference_weight: float = 1.0

    # -----------------------------
    # ADVANCED LOGIC
    # -----------------------------
    use_demand_penalty: bool = False
    demand_weight: float = 1.0

    forbidden_pairs: Optional[List[Tuple[str, str]]] = None
    balance_weight: float = 0.0

    # -----------------------------
    # LOGICAL CONSTRAINTS
    # -----------------------------
    mutual_exclusion: Optional[
        List[Tuple[Tuple[str, str], Tuple[str, str]]]
    ] = None

    implications: Optional[
        List[Tuple[Tuple[str, str], Tuple[str, str]]]
    ] = None

    group_limits: Optional[
        List[Tuple[List[Tuple[str, str]], int]]
    ] = None

    # -----------------------------
    # COVERAGE
    # -----------------------------
    enforce_full_coverage: bool = False
