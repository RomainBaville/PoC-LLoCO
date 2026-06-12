# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

def apply_ressources_constraints( model, x, problem ):
    if problem.use_costs:
        ressources_config = problem.ressources_config
        if ressources_config.max_vals is not None:
            for right_label in problem.right_labels:
                for ressources_labels, max_val in ressources_config.max_vals.items():
                    model.Add(
                        sum(
                            int( ressources_config.vals[ left_label, ressource_label ] ) * x[ left_label, right_label ] for ressource_label in ressources_labels for left_label in problem.left_entities
                        ) <= int( max_val )
                    )

        if ressources_config.min_vals is not None:
            for right_label in problem.right_labels:
                for ressources_labels, min_val in ressources_config.min_vals.items():
                    model.Add(
                        sum(
                            int( ressources_config.vals[ left_label, ressource_label ] ) * x[ left_label, right_label ] for ressource_label in ressources_labels for left_label in problem.left_entities
                        ) <= int( min_val )
                    )

        if ressources_config.max_vals_global is not None:
            for ressources_labels, max_val_global in ressources_config.max_vals_global.items():
                model.Add(
                    sum(
                        int( ressources_config.vals[ left_label, ressource_label ] ) * x[ left_label, right_label ] for ressource_label in ressources_labels for left_label, right_label in x
                    ) <= int( max_val_global )
                )

        if ressources_config.min_vals_global is not None:
            for ressources_labels, min_val_global in ressources_config.min_vals_global.items():
                model.Add(
                    sum(
                        int( ressources_config.vals[ left_label, ressource_label ] ) * x[ left_label, right_label ] for ressource_label in ressources_labels for left_label, right_label in x
                    ) <= int( min_val_global )
                )
