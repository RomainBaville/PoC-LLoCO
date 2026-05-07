# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from dataclasses import dataclass
from typing import Dict, List, Tuple
from domain.assignment.skills.base import SkillAssignmentProblem


@dataclass
class SkillPortfolioSelection(SkillAssignmentProblem):
    """
    Select a subset of entities whose combined skills cover requirements.
    """

    skill_requirements: Dict[str, int]

    def validate(self) -> None:
        for s in self.skills:
            self.skill_requirements.setdefault(s, 1)
