# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from typing_extensions import Self
from domain.assignment.score.score_config import ScoreConfig
from domain.assignment.constraints.constraints_config import ConstraintsConfig


class AssignmentProblem:
    """Class to deals with assignment problem."""

    def __init__(
        self: Self,
        left_labels: tuple[ str, ...],
        right_labels: tuple[ str, ...],
        score_config: ScoreConfig,
        constraints_config: ConstraintsConfig,
    ) -> None:
        """Initialisation of the class.

        Args:
            left_labels (tuple[str, ...]): The left entities labels to associate.
            right_labels (tuple[str, ...]): The right entities labels to associate.
            quantities_constraints (QuantitiesConstraints): All the quantities constraints of the assignment problem.
        """
        self.left_labels: tuple[ str, ...] = left_labels
        self.right_labels: tuple[ str, ... ] = right_labels

        self.score_config: ScoreConfig = score_config

        self.constraints_config: ConstraintsConfig = constraints_config

    def compute_matching_score(
        self: Self,
        left_label: str,
        right_label: str,
    ) -> float:
        """Compute the matching score for the problem for one left entity to one right entity.

        Args:
            left_label (str): The label of the left entity to evaluate.
            right_label (str): The label of the right entity to evaluate.

        Returns:
            float: The matching score for the left and right entities of the problem.
        """
        matching_score: float = 0
        if self.score_config.use_matching:
            matching_objective: int = self.score_config.matching_config.objective.value
            for matching_label in self.score_config.matching_config.labels:
                left_val: float = self.score_config.matching_config.left_vals[ ( left_label, matching_label ) ]
                right_val: float = self.score_config.matching_config.right_vals[ ( right_label, matching_label ) ]

                matching_weight: float = self.score_config.matching_config.weights[ matching_label ]
                reward: float = self.score_config.matching_config.reward_function( left_val, right_val )
                penalty: float = self.score_config.matching_config.penalty_function( left_val, right_val )

                matching_score +=  matching_objective * matching_weight * ( reward + penalty )

        return matching_score

    def compute_ressources_score(
        self: Self,
        left_label: str,
    ) -> float:
        """Compute the ressources score for one left entity of the problem.

        Args:
            left_label (str): The label of the left entity to evaluate.

        Returns:
            float: The ressources score for the left entity of the problem.
        """
        ressources_score: float = 0

        if self.score_config.use_ressources:
            for ressource_label in self.score_config.ressources_config.labels:
                val: float = self.score_config.ressources_config.vals[ ( left_label, ressource_label ) ]
                ressource_weight: float = self.score_config.ressources_config.weights[ ressource_label ]
                ressource_objective: int = self.score_config.ressources_config.objectives[ ressource_label ].value

                ressources_score += ressource_objective * ressource_weight * val

        return ressources_score
