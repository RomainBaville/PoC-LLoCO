# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from dataclasses import dataclass
from typing import List
from domain.base import DomainProblem


@dataclass
class AssignmentBaseProblem(DomainProblem):
    left_entities: List[str]
    right_entities: List[str]
