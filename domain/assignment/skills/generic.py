# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from dataclasses import dataclass
from typing import Dict, Tuple, List, Optional

from domain.assignment.config import AssignmentModelConfig


@dataclass
class SkillAssignmentProblem:
    left_entities: List[str]
    right_entities: List[str]
    skills: List[str]

    left_skills: Dict[Tuple[str, str], int]
    right_requirements: Dict[Tuple[str, str], int]

    config: AssignmentModelConfig

    costs: Optional[Dict[Tuple[str, str], float]] = None
    preferences: Optional[Dict[Tuple[str, str], float]] = None

    def validate(self):
        for l in self.left_entities:
            for s in self.skills:
                self.left_skills.setdefault((l, s), 0)

        for r in self.right_entities:
            for s in self.skills:
                self.right_requirements.setdefault((r, s), 0)

        if self.config.skill_weights is None:
            self.config.skill_weights = {}
            for s in self.skills:
                self.config.skill_weights[ s ] = 1
