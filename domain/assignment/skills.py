# SPDX-License-Identifier: Apache-2.0
from dataclasses import dataclass
from typing import Dict, Tuple, List
from domain.assignment.base import AssignmentBaseProblem


@dataclass
class SkillBasedAssignmentProblem(AssignmentBaseProblem):
    skills: List[str]
    left_skills: Dict[Tuple[str, str], int]
    right_requirements: Dict[Tuple[str, str], int]
    max_assignments_per_left: int = 1

    def validate(self):
        for l in self.left_entities:
            for s in self.skills:
                self.left_skills.setdefault((l, s), 0)

        for r in self.right_entities:
            for s in self.skills:
                self.right_requirements.setdefault((r, s), 0)
