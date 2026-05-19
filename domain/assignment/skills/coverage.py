# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from dataclasses import dataclass
from typing import Dict, Tuple

from domain.assignment.skills.base import SkillAssignmentProblem


@dataclass
class SkillCoverageAssignment(SkillAssignmentProblem):
    """
    Assign entities so that all required skills are covered.
    """

    right_requirements: Dict[Tuple[str, str], int]
    max_assignments_per_left: int = 1

    def validate(self) -> None:
        for l in self.left_entities:
            for s in self.skills:
                self.left_skills.setdefault((l, s), 0)

        for r in self.right_entities:
            for s in self.skills:
                self.right_requirements.setdefault((r, s), 0)
