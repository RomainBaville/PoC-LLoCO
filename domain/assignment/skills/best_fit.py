# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from dataclasses import dataclass
from typing import Dict, List, Tuple
from domain.assignment.skills.base import SkillAssignmentProblem


@dataclass
class SkillBestFitAssignment(SkillAssignmentProblem):
    """
    Match entities to targets to maximize skill similarity.
    """

    target_preferences: Dict[Tuple[str, str], int]
    max_assignments_per_left: int = 1

    def validate(self) -> None:
        for l in self.left_entities:
            for s in self.skills:
                self.left_skills.setdefault((l, s), 0)
