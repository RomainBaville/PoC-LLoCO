# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from domain.assignment.base import AssignmentProblem

def apply_ressources_constraints( model, x, problem: AssignmentProblem ):
    if problem.use_ressources:
        if problem.ressources_config.max_vals is not None:
            for key in problem.ressources_config.max_vals:
                right_label = key[ 0 ]
                ressources_labels = key[ 1: ]
                max_val = int( problem.ressources_config.max_vals[ key ] )
                model.Add(
                    sum(
                        int( problem.ressources_config.vals[ left_label, ressource_label ] ) * x[ left_label, right_label ] for ressource_label in ressources_labels for left_label in problem.left_labels
                    ) <= max_val
                )

        if problem.ressources_config.min_vals is not None:
            for key in problem.ressources_config.min_vals:
                right_label = key[ 0 ]
                ressources_labels = key[ 1: ]
                min_val = int( problem.ressources_config.min_vals[ key ] )
                model.Add(
                    sum(
                        int( problem.ressources_config.vals[ left_label, ressource_label ] ) * x[ left_label, right_label ] for ressource_label in ressources_labels for left_label in problem.left_labels
                    ) >= min_val
                )

        if problem.ressources_config.max_vals_global is not None:
            for ressources_labels, max_val_global in problem.ressources_config.max_vals_global.items():
                model.Add(
                    sum(
                        int( problem.ressources_config.vals[ left_label, ressource_label ] ) * x[ left_label, right_label ] for ressource_label in ressources_labels for left_label, right_label in x
                    ) <= int( max_val_global )
                )

        if problem.ressources_config.min_vals_global is not None:
            for ressources_labels, min_val_global in problem.ressources_config.min_vals_global.items():
                model.Add(
                    sum(
                        int( problem.ressources_config.vals[ left_label, ressource_label ] ) * x[ left_label, right_label ] for ressource_label in ressources_labels for left_label, right_label in x
                    ) >= int( min_val_global )
                )
