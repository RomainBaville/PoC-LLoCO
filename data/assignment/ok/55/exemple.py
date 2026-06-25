# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

import sys
from pathlib import Path

# --- make project root importable ---
ROOT_DIR = Path( __file__ ).resolve().parents[ 4 ]
sys.path.append( str( ROOT_DIR ) )

from domain.objective import Objective
from domain.assignment.base import AssignmentProblem
from domain.assignment.score.score_config import ScoreConfig
from domain.assignment.score.ressources_config import RessourcesConfig
from domain.assignment.constraints.constraints_config import ConstraintsConfig
from domain.assignment.constraints.logicals_constraints import LogicalsConstraints
from domain.assignment.constraints.quantities_constraints import QuantitiesConstraints
from solvers.assignment.cp_model.ortools_cp_sat import solve_assignment_problem


# Base
left_labels = [ "Calculus", "OperationsResearch", "DataStructures", "ManagementStatistics", "ComputerSimulation", "ComputerProgramming", "Forecasting" ]
right_labels = [ "Student" ]

# Score
labels = [ "Mathematics", "ComputerScience", "OperationsResearch" ]
vals = {
    ( "Calculus", "Mathematics" ): 1,
    ( "Calculus", "ComputerScience" ): 0,
    ( "Calculus", "OperationsResearch" ): 0,
    ( "OperationsResearch", "Mathematics" ): 1,
    ( "OperationsResearch", "ComputerScience" ): 0,
    ( "OperationsResearch", "OperationsResearch" ): 1,
    ( "DataStructures", "Mathematics" ): 1,
    ( "DataStructures", "ComputerScience" ): 1,
    ( "DataStructures", "OperationsResearch" ): 0,
    ( "ManagementStatistics", "Mathematics" ): 1,
    ( "ManagementStatistics", "ComputerScience" ): 0,
    ( "ManagementStatistics", "OperationsResearch" ): 1,
    ( "ComputerSimulation", "Mathematics" ): 0,
    ( "ComputerSimulation", "ComputerScience" ): 1,
    ( "ComputerSimulation", "OperationsResearch" ): 1,
    ( "ComputerProgramming", "Mathematics" ): 0,
    ( "ComputerProgramming", "ComputerScience" ): 1,
    ( "ComputerProgramming", "OperationsResearch" ): 0,
    ( "Forecasting", "Mathematics" ): 1,
    ( "Forecasting", "ComputerScience" ): 0,
    ( "Forecasting", "OperationsResearch" ): 1,
}
objectives = {
    "Mathematics": Objective.MINIMIZE,
    "ComputerScience": Objective.MINIMIZE,
    "OperationsResearch": Objective.MINIMIZE,
}
weights = {
    "Mathematics": 1,
    "ComputerScience": 1,
    "OperationsResearch": 1,
}
min_val = {
    ( "Student", "Mathematics" ): 2,
    ( "Student", "ComputerScience" ): 2,
    ( "Student", "OperationsResearch" ): 2,
}
use_ressources = True
ressouces_config = RessourcesConfig(
    labels=labels,
    vals=vals,
    objectives=objectives,
    weights=weights,
    min_vals=min_val,
)
score_config = ScoreConfig(
    use_ressources=use_ressources,
    ressources_config=ressouces_config,
)

# Constraints
use_quantities_constraints = True
multiple_same_assignment = False
quantities_constraints = QuantitiesConstraints(
    multiple_same_assignment=multiple_same_assignment,
)
use_logical_constraints = True
implications = {
    ( "DataStructures", "Student" ): ( ( "ComputerProgramming", "Student", 1 ), ),
    ( "ComputerSimulation", "Student" ): ( ( "ComputerProgramming", "Student", 1 ), ),
    ( "ManagementStatistics", "Student" ): ( ( "Calculus", "Student", 1 ), ),
    ( "Forecasting", "Student" ): ( ( "ManagementStatistics", "Student", 1 ), ),
}
logicals_constraints = LogicalsConstraints(
    implications=implications,
)
constraints_config = ConstraintsConfig(
    use_logicals_constraints=use_logical_constraints,
    logicals_constraints=logicals_constraints,
    use_quantities_constraints=use_quantities_constraints,
    quantities_constraints=quantities_constraints,
)

problem: AssignmentProblem = AssignmentProblem(
    left_labels=left_labels,
    right_labels=right_labels,
    score_config=score_config,
    constraints_config=constraints_config
)


solutions = solve_assignment_problem( problem )

print( solutions )
