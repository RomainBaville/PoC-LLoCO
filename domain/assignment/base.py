# SPDX-License-Identifier: Apache-2.0
from dataclasses import dataclass
from typing import List
from domain.base import DomainProblem


@dataclass
class AssignmentBaseProblem(DomainProblem):
    left_entities: List[str]
    right_entities: List[str]
