# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass
class AssignmentStructure:
    """
    Generic bipartite assignment structure.
    No business semantics here.
    """

    left_entities: List[str]
    right_entities: List[str]
    attributes: List[str]

    left_attributes: Dict[Tuple[str, str], int]
    right_requirements: Dict[Tuple[str, str], int]

    max_left_assignments: int = 1

    def validate(self):
        for l in self.left_entities:
            for a in self.attributes:
                self.left_attributes.setdefault((l, a), 0)

        for r in self.right_entities:
            for a in self.attributes:
                self.right_requirements.setdefault((r, a), 0)
