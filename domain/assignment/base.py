# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from dataclasses import dataclass
from typing import Optional
from domain.assignment.matching.matching_config import MatchingConfig
from domain.assignment.single.single_config import SingleConfig


@dataclass
class AssignmentProblem:
    left_labels: list[ str ]
    right_labels: list[ str ]

    # Scoring
    use_matching: bool = False
    matching_config: Optional[ MatchingConfig ] = None

    use_single: bool = False
    single_config: Optional[ SingleConfig ] = None

    # Global constraints
    max_assignments: Optional[ dict[ str, int ] ] = None
    min_assignments: Optional[ dict[ str, int ] ] = None

    max_capacities: Optional[ dict[ str, int ] ] = None
    min_capacities: Optional[ dict[ str, int ] ] = None

    left_mutual_exclusions: Optional[ list[ list[ str ] ] ] = None
    right_mutual_exclusions: Optional[ list[ list[ str ] ] ] = None
