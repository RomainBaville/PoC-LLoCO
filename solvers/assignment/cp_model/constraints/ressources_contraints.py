# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from ortools.sat.python.cp_model import CpModel, IntVar

from domain.assignment.score.ressources_config import RessourcesConfig


def apply_ressources_constraints(
    model: CpModel,
    quantities: dict[ tuple[ str, str ], IntVar ],
    ressources_config: RessourcesConfig,
    left_labels: tuple[ str, ...]
) -> None:
    """Add to the model the ressources constraints if needed.

    Args:
        model (CpModel): The model used.
        quantities (dict[tuple[str, str], IntVar]): The integrable variable with the number of assocciation.
        ressources_config (RessourcesConfig): The ressources config with the constraints of the assignment problem.
        left_labels (tuple[str, ...]): The left entities labels.
    """
    if isinstance( ressources_config.max_vals, dict ):
        for key in ressources_config.max_vals:
            right_label = key[ 0 ]
            ressources_labels = key[ 1: ]
            max_val = int( ressources_config.max_vals[ key ] )
            model.add(
                sum(
                    int( ressources_config.vals[ left_label, ressource_label ] ) *
                    quantities[ left_label, right_label ]
                    for ressource_label in ressources_labels
                    for left_label in left_labels
                ) <= max_val
            )

    if isinstance( ressources_config.min_vals, dict ):
        for key in ressources_config.min_vals:
            right_label = key[ 0 ]
            ressources_labels = key[ 1: ]
            min_val = int( ressources_config.min_vals[ key ] )
            model.add(
                sum(
                    int( ressources_config.vals[ left_label, ressource_label ] ) *
                    quantities[ left_label, right_label ]
                    for ressource_label in ressources_labels
                    for left_label in left_labels
                ) >= min_val
            )

    if isinstance( ressources_config.max_global_vals, dict ):
        for ressources_labels, max_global_val in ressources_config.max_global_vals.items():
            model.add(
                sum(
                    int( ressources_config.vals[ left_label, ressource_label ] ) *
                    quantities[ left_label, right_label ]
                    for ressource_label in ressources_labels
                    for left_label, right_label in quantities
                ) <= int( max_global_val )
            )

    if isinstance( ressources_config.min_global_vals, dict ):
        for ressources_labels, min_global_val in ressources_config.min_global_vals.items():
            model.add(
                sum(
                    int( ressources_config.vals[ left_label, ressource_label ] ) *
                    quantities[ left_label, right_label ]
                    for ressource_label in ressources_labels
                    for left_label, right_label in quantities
                ) >= int( min_global_val )
            )
