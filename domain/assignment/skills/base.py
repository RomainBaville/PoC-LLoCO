# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from dataclasses import dataclass
from typing import Dict, List, Tuple
from abc import ABC
from domain.assignment.base import AssignmentBaseProblem


@dataclass
class SkillAssignmentProblem(AssignmentBaseProblem, ABC):
    """
    Base class for all skill-based assignment problems.
    Declares all common fields so dataclass inheritance works correctly.
    """

    skills: List[str]
    left_skills: Dict[Tuple[str, str], int]
