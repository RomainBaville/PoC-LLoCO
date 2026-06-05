# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from dataclasses import dataclass
from typing import Optional
from domain.assignment.skills.skills_config import SkillsConfig


@dataclass
class AssignmentProblem:
    left_entities: list[ str ]
    right_entities: list[ str ]

    min_assignments_per_left: Optional[ dict[ str, int ] ] = None
    max_assignments_per_left: Optional[ dict[ str, int ] ] = None

    min_capacities_per_right: Optional[ dict[ str, int ] ] = None
    max_capacities_per_right: Optional[ dict[ str, int ] ] = None

    left_mutual_exclusions: Optional[ list[ list[ str ] ] ] = None
    right_mutual_exclusions: Optional[ list[ list[ str ] ] ] = None

    use_skills: bool = False
    skills_config: Optional[ SkillsConfig ] = None
