# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville


from dataclasses import dataclass
from typing import Dict, Tuple, Optional

from domain.assignment.skills.base import SkillAssignmentProblem


# --------------------------------------------------
# Configuration object
# --------------------------------------------------

@dataclass
class BestFitConfig:
    max_assignments_per_left: int = 1
    max_assignments_per_right: Optional[int] = None

    # scoring system
    reward_mode: str = "min"
    penalty_mode: Optional[str] = None
    penalty_weight: float = 1.0

    skill_weights: Optional[Dict[str, float]] = None



# --------------------------------------------------
# Problem definition
# --------------------------------------------------

@dataclass
class SkillBestFitAssignment(SkillAssignmentProblem):
    """
    Generic best-fit assignment:
    maximize compatibility between left entities and right entities.
    """

    target_preferences: Dict[Tuple[str, str], int]
    config: BestFitConfig

    def validate(self) -> None:
        # Ensure all skill entries exist
        for l in self.left_entities:
            for s in self.skills:
                self.left_skills.setdefault((l, s), 0)

        for r in self.right_entities:
            for s in self.skills:
                self.target_preferences.setdefault((r, s), 0)

        # Default weights
        if self.config.skill_weights is None:
            self.config.skill_weights = {s: 1.0 for s in self.skills}
