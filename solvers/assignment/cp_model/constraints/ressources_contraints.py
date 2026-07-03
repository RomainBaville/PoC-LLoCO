# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from ortools.sat.python.cp_model import CpModel, IntVar

from domain.assignment.base import AssignmentProblem
from domain.assignment.score.ressources_config import RessourcesConfig


def apply_ressources_constraints(
    model: CpModel,
    quantities: dict[ tuple[ str, str ], IntVar ],
    problem: AssignmentProblem,
) -> None:
    """Add to the model the quantities constraints if needed.

    Args:
        model (CpModel): The model used.
        quantities (dict[tuple[str, str], IntVar]): The integrable variable with the number of assocciation.
        problem (AssignmentProblem): The assignment problem.
    """
    if problem.score_config.use_ressources:
        ressources_config: RessourcesConfig = problem.score_config.ressources_config
        if ressources_config.max_vals is not None:
            for key in ressources_config.max_vals:
                right_label = key[ 0 ]
                ressources_labels = key[ 1: ]
                max_val = int( ressources_config.max_vals[ key ] )
                model.Add(
                    sum(
                        int( ressources_config.vals[ left_label,
                                                    ressource_label ] ) * quantities[ left_label, right_label ]
                        for ressource_label in ressources_labels
                        for left_label in problem.left_labels
                    ) <= max_val
                )

        if ressources_config.min_vals is not None:
            for key in ressources_config.min_vals:
                right_label = key[ 0 ]
                ressources_labels = key[ 1: ]
                min_val = int( ressources_config.min_vals[ key ] )
                model.Add(
                    sum(
                        int( ressources_config.vals[ left_label,
                                                    ressource_label ] ) * quantities[ left_label, right_label ]
                        for ressource_label in ressources_labels
                        for left_label in problem.left_labels
                    ) >= min_val
                )

        if ressources_config.max_global_vals is not None:
            for ressources_labels, max_global_val in ressources_config.max_global_vals.items():
                model.Add(
                    sum(
                        int( ressources_config.vals[ left_label,
                                                    ressource_label ] ) * quantities[ left_label, right_label ]
                        for ressource_label in ressources_labels
                        for left_label, right_label in quantities
                    ) <= int( max_global_val )
                )

        if ressources_config.min_global_vals is not None:
            for ressources_labels, min_global_val in ressources_config.min_global_vals.items():
                model.Add(
                    sum(
                        int( ressources_config.vals[ left_label,
                                                    ressource_label ] ) * quantities[ left_label, right_label ]
                        for ressource_label in ressources_labels
                        for left_label, right_label in quantities
                    ) >= int( min_global_val )
                )
