# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from typing_extensions import Optional, Self
from domain.assignment.matching.matching_config import MatchingConfig
from domain.assignment.ressources.ressources_config import RessourcesConfig


class AssignmentProblem:

    def __init__(
        self: Self,
        left_labels: list[ str ],
        right_labels: list[ str ],
        use_matching: bool = False,
        matching_config: Optional[ MatchingConfig ] = None,
        use_ressources: bool = False,
        ressources_config: Optional[ RessourcesConfig ] = None,
        max_assignments: Optional[ dict[ str, float ] ] = None,
        min_assignments: Optional[ dict[ str, float ] ] = None,
        max_capacities: Optional[ dict[ str, float ] ] = None,
        min_capacities: Optional[ dict[ str, float ] ] = None,
        left_mutual_exclusions: Optional[ list[ list[ str ] ] ] = None,
        right_mutual_exclusions: Optional[ list[ list[ str ] ] ] = None,
    ) -> None:
        """Class to deals with assignment problem.

        Args:
            left_labels (list[str]): The list of the left entities labels to associate.
            right_labels (list[str]): The list of the right entities labels to associate.
            use_matching (bool): True if the problem needs to match left and right entities (e.g. skills, production ...):
                Defaults to False.
            matching_config (Optional[MatchingConfig]): The configuration of the matching to make.
            use_ressources (bool): True if the problem needs to optimize left entities ressources (e.g. salary, time ...):
                Defaults to False.
            ressources_config (Optional[RessourcesConfig]): The configuration of the ressources to use.
            max_assignments (Optional[dict[str, float]]): The dictionary whit the maximum assignments accepted per left entities:
                - keys (str): The left entity label.
                - value (float): The maximum assignments accepted by the left entity.
            min_assignments (Optional[dict[str, float]]): The dictionary whit the minimum assignments accepted per left entities:
                - keys (str): The left entity label.
                - value (float): The minimum assignments accepted by the left entity.
            max_capacities (Optional[dict[str, float]]): The dictionary whit the maximum capacities accepted per right entities:
                - keys (str): The right entity label.
                - value (float): The maximum capacities accepted by the right entity.
            min_capacities (Optional[dict[str, float]]): The dictionary whit the minimum capacities accepted per right entities:
                - keys (str): The right entity label.
                - value (float): The minimum capacities accepted by the right entity.
            left_mutual_exclusions (Optional[list[list[str]]]): The list of left entities groups that can't be associated together.
            right_mutual_exclusions (Optional[list[list[str]]]): The list of right entities groups that can't be assigned together.
        """
        self.left_labels: list[ str ] = left_labels
        self.right_labels: list[ str ] = right_labels

        # Scoring
        self.use_matching: bool = use_matching
        self.matching_config: Optional[ MatchingConfig ] = matching_config

        self.use_ressources: bool = use_ressources
        self.ressources_config: Optional[ RessourcesConfig ] = ressources_config

        # Generic constraints
        self.max_assignments: Optional[ dict[ str, float ] ] = max_assignments
        self.min_assignments: Optional[ dict[ str, float ] ] = min_assignments

        self.max_capacities: Optional[ dict[ str, float ] ] = max_capacities
        self.min_capacities: Optional[ dict[ str, float ] ] = min_capacities

        # Logical constraints
        self.left_mutual_exclusions: Optional[ list[ list[ str ] ] ] = left_mutual_exclusions
        self.right_mutual_exclusions: Optional[ list[ list[ str ] ] ] = right_mutual_exclusions

    def compute_score(
        self: Self,
        left_label: str,
        right_label: str,
    ) -> float:
        """Compute the assignment score for the problem for one left entity to one right entity.

        Args:
            left_label (str): The label of the left entity to evaluate.
            right_label (str): The label of the right entity to evaluate.

        Returns:
            score (float): The assignment score for the left and right entities of the problem.
        """
        score: float = 0

        if self.use_matching:
            for matching_label in self.matching_config.labels:
                left_val = self.matching_config.left_vals[ ( left_label, matching_label ) ]
                right_val = self.matching_config.right_vals[ ( right_label, matching_label ) ]

                matching_weight: float = 1.
                if self.matching_config.weights is not None:
                    if matching_label in self.matching_config.weights:
                        matching_weight = self.matching_config.weights[ matching_label ]

                reward: float = self.matching_config.reward_function( left_val, right_val )
                penalty: float = self.matching_config.penalty_function( left_val, right_val )

                score += self.matching_config.objective.value * matching_weight * ( reward + penalty )

        if self.use_ressources:
            for ressource_label in self.ressources_config.labels:
                weight: float = 1.
                if self.ressources_config.weights is not None:
                    if ressource_label in self.ressources_config.weights:
                        weight = self.ressources_config.weights[ ressource_label ]

                score += self.ressources_config.objectives[ ressource_label ].value * weight * self.ressources_config.vals[ ( left_label, ressource_label ) ]

        return score
