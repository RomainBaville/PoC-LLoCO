# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from dataclasses import dataclass
from typing import Dict, List, Tuple
from domain.assignment.skills.base import SkillAssignmentProblem


@dataclass
class SkillTeamAssignment(SkillAssignmentProblem):
    """
    Assign MULTIPLE entities to a target so the TEAM covers skills.
    """

    team_requirements: Dict[Tuple[str, str], int]
    min_team_size: Dict[str, int]
    max_team_size: Dict[str, int]

    def validate(self) -> None:
        for r in self.right_entities:
            self.min_team_size.setdefault(r, 1)
            self.max_team_size.setdefault(r, len(self.left_entities))
