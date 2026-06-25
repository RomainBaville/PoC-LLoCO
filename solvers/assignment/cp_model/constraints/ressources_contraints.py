# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from domain.assignment.base import AssignmentProblem
from ortools.sat.python.cp_model import CpModel, IntVar
from domain.assignment.score.ressources_config import RessourcesConfig

def apply_ressources_constraints(
    model: CpModel,
    var: dict[ tuple[ str, str ], IntVar ],
    problem: AssignmentProblem,
) -> None:
    if problem.score_config.use_ressources:
        ressources_config: RessourcesConfig = problem.score_config.ressources_config
        if ressources_config.max_vals is not None:
            for key in ressources_config.max_vals:
                right_label = key[ 0 ]
                ressources_labels = key[ 1: ]
                max_val = int( ressources_config.max_vals[ key ] )
                model.Add(
                    sum(
                        int( ressources_config.vals[ left_label, ressource_label ] ) * var[ left_label, right_label ] for ressource_label in ressources_labels for left_label in problem.left_labels
                    ) <= max_val
                )

        if ressources_config.min_vals is not None:
            for key in ressources_config.min_vals:
                right_label = key[ 0 ]
                ressources_labels = key[ 1: ]
                min_val = int( ressources_config.min_vals[ key ] )
                model.Add(
                    sum(
                        int( ressources_config.vals[ left_label, ressource_label ] ) * var[ left_label, right_label ] for ressource_label in ressources_labels for left_label in problem.left_labels
                    ) >= min_val
                )

        if ressources_config.max_global_vals is not None:
            for ressources_labels, max_global_val in ressources_config.max_global_vals.items():
                model.Add(
                    sum(
                        int( ressources_config.vals[ left_label, ressource_label ] ) * var[ left_label, right_label ] for ressource_label in ressources_labels for left_label, right_label in var
                    ) <= int( max_global_val )
                )

        if ressources_config.min_global_vals is not None:
            for ressources_labels, min_global_val in ressources_config.min_global_vals.items():
                model.Add(
                    sum(
                        int( ressources_config.vals[ left_label, ressource_label ] ) * var[ left_label, right_label ] for ressource_label in ressources_labels for left_label, right_label in var
                    ) >= int( min_global_val )
                )
