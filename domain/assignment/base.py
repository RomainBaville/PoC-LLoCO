# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from typing_extensions import Optional, Self
from domain.assignment.matching.matching_config import MatchingConfig
from domain.assignment.ressources.ressources_config import RessourcesConfig


class AssignmentProblem:

    def __init__(
        self: Self,
        left_labels: tuple[ str, ...],
        right_labels: tuple[ str, ...],
        use_matching: bool = False,
        matching_config: Optional[ MatchingConfig ] = None,
        use_ressources: bool = False,
        ressources_config: Optional[ RessourcesConfig ] = None,
        max_several_assignments: Optional[ dict[ str, float ] ] = None,
        min_several_assignments: Optional[ dict[ str, float ] ] = None,
        max_assignments: Optional[ dict[ tuple[ str, str ], float ] ] = None,
        min_assignments: Optional[ dict[ tuple[ str, str ], float ] ] = None,
        max_assignments_global: Optional[ dict[ str, float ] ] = None,
        min_assignments_global: Optional[ dict[ str, float ] ] = None,
        max_several_capacities: Optional[ dict[ str, float ] ] = None,
        min_several_capacities: Optional[ dict[ str, float ] ] = None,
        max_capacities: Optional[ dict[ tuple[ str, str ], float ] ] = None,
        min_capacities: Optional[ dict[ tuple[ str, str ], float ] ] = None,
        max_capacities_global: Optional[ dict[ str, float ] ] = None,
        min_capacities_global: Optional[ dict[ str, float ] ] = None,
        left_mutual_exclusions: Optional[ tuple[ tuple[ str, ...], ...] ] = None,
        right_mutual_exclusions: Optional[ tuple[ tuple[ str, ...], ...] ] = None,
        implications: Optional[ dict[ tuple[ str, str ], tuple[ tuple[ str, str, Optional[ float ] ], ...] ] ] = None,
    ) -> None:
        """Class to deals with assignment problem.

        Args:
            left_labels (tuple[str, ...]): The left entities labels to associate.
            right_labels (tuple[str, ...]): The right entities labels to associate.
            use_matching (bool): True if the problem optimization score uses left and right entities matching (e.g. skills, production ...):
                Defaults to False.
            matching_config (Optional[MatchingConfig]): The configuration of the matching to make.
            use_ressources (bool): True if the problem optimisation score uses left entities ressources (e.g. salary, time ...):
                Defaults to False.
            ressources_config (Optional[RessourcesConfig]): The configuration of the ressources to use.
            max_several_assignments (Optional[dict[str, float]]): The dictionary with the maximum number of several right entities, a left entity can be assigned:
                - keys (str): The left entity label.
                - values (float): The maximum number of several right entities allowed.
            min_several_assignments (Optional[dict[str, float]]): The dictionary with the minimum number of several right entities, a left entity can be assigned:
                - keys (str): The left entity label.
                - values (float): The minimum number of several right entities allowed.
            max_assignments (Optional[dict[tuple[str, str], float]]): The dictionary whit the maximum number of assignments allowed by left entities per right entities:
                - keys (tuple[str, str]): The left and right entity labels.
                - value (float): The maximum number of assignments allowed by the left entity for the right entity.
            min_assignments (Optional[dict[tuple[str, str], float]]): The dictionary whit the minimum number of assignments allowed by left entities per right entities:
                - keys (tuple[str, str]): The left and right entity labels.
                - value (float): The minimum number of assignments allowed by the left entity for the right entity.
            max_assignments_global (Optional[dict[str, float]]): The dictionary whit the maximum number of assignments allowed per left entities:
                - keys (str): The left entity label.
                - value (float): The maximum number of assignments allowed for the left entity.
            min_assignments_global (Optional[dict[str, float]]): The dictionary whit the minimum number of assignments allowed per left entities:
                - keys (str): The left entity label.
                - value (float): The minimum number of assignments allowed for the left entity.
            max_several_capacities (Optional[dict[str, float]]): The dictionary with the maximum number of several left entities, a right entity can handled:
                - keys (str): The right entity label.
                - values (float): The maximum number of several left entities allowed.
            min_several_capacities (Optional[dict[str, float]]): The dictionary with the minimum number of several left entities, a right entity can handled:
                - keys (str): The right entity label.
                - values (float): The minimum number of several left entities allowed.
            max_capacities (Optional[dict[tuple[str, str], float]]): The dictionary whit the maximum number of assignments allowed by right entities per left entities:
                - keys (tuple[str, str]): The left and right entity labels.
                - value (float): The maximum number of assignments allowed by the right entity for the left entity.
            min_capacities (Optional[dict[tuple[str, str], float]]): The dictionary whit the minimum number of assignments allowed by right entities per left entities:
                - keys (tuple[str, str]): The left and right entity labels.
                - value (float): The minimum number of assignments allowed by the right entity for the left entity.
            max_capacities_global (Optional[dict[str, float]]): The dictionary whit the maximum number of assignments allowed per right entities:
                - keys (str): The right entity label.
                - value (float): The maximum number of assignments allowed for the right entity.
            min_capacities_global (Optional[dict[str, float]]): The dictionary whit the minimum number of assignments allowed per right entities:
                - keys (str): The right entity label.
                - value (float): The minimum number of assignments allowed for the right entity.
            left_mutual_exclusions (Optional[tuple[tuple[str, ...], ...]]): Groups of left entity labels that can't be associated together.
            right_mutual_exclusions (Optional[tuple[tuple[str, ...], ...]]): Groups of right entity labels that can't be assigned together.
            implications (Optional[dict[tuple[str, str], tuple[tuple[str, str, Optional[float]], ...]]]): The dictionary with the implication of an association:
                - keys (tuple[str, str]): The left and right entity labels of the association with an implication.
                - values (tuple[tuple[str, str, Optional[float]], ...]]): The several left and rigth label of the implicated association with the number of forced associations.
        """
        self.left_labels: tuple[ str, ...] = left_labels
        self.right_labels: tuple[ str, ... ] = right_labels

        # Scoring
        self.use_matching: bool = use_matching
        self.matching_config: Optional[ MatchingConfig ] = matching_config

        self.use_ressources: bool = use_ressources
        self.ressources_config: Optional[ RessourcesConfig ] = ressources_config

        # Quantity constraints
        self.max_several_assignments: Optional[ dict[ str, float ] ] = max_several_assignments
        self.min_several_assignments: Optional[ dict[ str, float ] ] = min_several_assignments

        self.max_assignments: Optional[ dict[ tuple[ str, str ], float ] ] = max_assignments
        self.min_assignments: Optional[ dict[ tuple[ str, str ], float ] ] = min_assignments

        self.max_assignments_global: Optional[ dict[ str, float ] ] = max_assignments_global
        self.min_assignments_global: Optional[ dict[ str, float ] ] = min_assignments_global

        self.max_several_capacities: Optional[ dict[ str, float ] ] = max_several_capacities
        self.min_several_capacities: Optional[ dict[ str, float ] ] = min_several_capacities

        self.max_capacities: Optional[ dict[ tuple[ str, str ], float ] ] = max_capacities
        self.min_capacities: Optional[ dict[ tuple[ str, str ], float ] ] = min_capacities

        self.max_capacities_global: Optional[ dict[ str, float ] ] = max_capacities_global
        self.min_capacities_global: Optional[ dict[ str, float ] ] = min_capacities_global



        # Logical constraints
        self.left_mutual_exclusions: Optional[ tuple[ tuple[ str, ...], ...] ] = left_mutual_exclusions
        self.right_mutual_exclusions: Optional[ tuple[ tuple[ str, ...], ...] ] = right_mutual_exclusions

        self.implications: Optional[ dict[ tuple[ str, str ], tuple[ tuple[ str, str, Optional[ float ] ], ...] ] ] = implications

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
        if self.use_matching:
            matching_objective: int = self.matching_config.objective.value
            for matching_label in self.matching_config.labels:
                left_val: float = self.matching_config.left_vals[ ( left_label, matching_label ) ]
                right_val: float = self.matching_config.right_vals[ ( right_label, matching_label ) ]

                matching_weight: float = self.matching_config.weights[ matching_label ]
                reward: float = self.matching_config.reward_function( left_val, right_val )
                penalty: float = self.matching_config.penalty_function( left_val, right_val )

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

        if self.use_ressources:
            for ressource_label in self.ressources_config.labels:
                val: float = self.ressources_config.vals[ ( left_label, ressource_label ) ]
                ressource_weight: float = self.ressources_config.weights[ ressource_label ]
                ressource_objective: int = self.ressources_config.objectives[ ressource_label ].value

                ressources_score += ressource_objective * ressource_weight * val

        return ressources_score
