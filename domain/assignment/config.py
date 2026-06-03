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
    min_assignments_per_left: Optional[Dict[str, int]] = None
    max_assignments_per_left: Optional[Dict[str, int]] = None

    min_capacities_per_right: Optional[Dict[str, int]] = None
    max_capacities_per_right: Optional[Dict[str, int]] = None

    # -----------------------------
    # OBJECTIVE
    # -----------------------------
    objective: str = "maximize"

    reward_mode: str = "min"
    penalty_mode: Optional[str] = None
    penalty_weight: float = 1.0
    skill_weights: Optional[Dict[str, float]] = None

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
