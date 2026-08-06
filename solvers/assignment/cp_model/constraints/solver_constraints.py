# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from ortools.sat.python.cp_model import CpModel, IntVar

from domain.assignment.base import AssignmentProblem
from domain.assignment.constraints.logicals_constraints import LogicalsConstraints
from domain.assignment.constraints.quantities_constraints import QuantitiesConstraints
from domain.assignment.score.matching_config import MatchingConfig
from domain.assignment.score.ressources_config import RessourcesConfig
from solvers.assignment.cp_model.constraints.logical_constraints import apply_logical_constraints
from solvers.assignment.cp_model.constraints.matching_constraints import apply_matching_constraints
from solvers.assignment.cp_model.constraints.quantities_constraints import apply_quantities_constraints
from solvers.assignment.cp_model.constraints.ressources_contraints import apply_ressources_constraints


def apply_constraints(
    model: CpModel,
    is_assigned: dict[ tuple[ str, str ], IntVar ],
    quantities: dict[ tuple[ str, str ], IntVar ],
    problem: AssignmentProblem
) -> None:
    """Add to the model all the constraints if needed.

    Args:
        model (CpModel): The model used.
        is_assigned (dict[tuple[str, str], IntVar]): The binary variable with 1 for assigned 0 otherwize.
        quantities (dict[tuple[str, str], IntVar]): The integrable variable with the number of assocciation.
        problem (AssignmentProblem): The assignment problem.
    """
    if not problem.constraints_config.multiple_same_assignment:
        for left_label, right_label in quantities:
            model.add( quantities[ left_label, right_label ] <= 1 )

    if isinstance( problem.constraints_config.quantities_constraints, QuantitiesConstraints ):
        quantities_constraints: QuantitiesConstraints = problem.constraints_config.quantities_constraints
        apply_quantities_constraints(
            model=model,
            is_assigned=is_assigned,
            quantities=quantities,
            quantities_constraints=quantities_constraints,
            left_labels=problem.left_labels,
            right_labels=problem.right_labels,
            multiple_same_assignment=problem.constraints_config.multiple_same_assignment
        )

    if isinstance( problem.constraints_config.logicals_constraints, LogicalsConstraints ):
        logicals_constraints: LogicalsConstraints = problem.constraints_config.logicals_constraints
        apply_logical_constraints(
            model=model,
            is_assigned=is_assigned,
            quantities=quantities,
            logicals_constraints=logicals_constraints,
            left_labels=problem.left_labels,
            right_labels=problem.right_labels
        )

    if isinstance( problem.score_config.matching_config, MatchingConfig ):
        matching_config: MatchingConfig = problem.score_config.matching_config
        apply_matching_constraints(
            model=model, is_assigned=is_assigned, matching_config=matching_config, left_labels=problem.left_labels
        )

    if isinstance( problem.score_config.ressources_config, RessourcesConfig ):
        ressources_config: RessourcesConfig = problem.score_config.ressources_config
        apply_ressources_constraints(
            model=model, quantities=quantities, ressources_config=ressources_config, left_labels=problem.left_labels
        )
