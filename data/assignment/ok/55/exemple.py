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
from domain.assignment.ressources.ressources_config import RessourcesConfig
from solvers.assignment.cp_model.ortools_cp_sat import ORToolsAssignmentSolver

left = [ "Calculus", "OperationsResearch", "DataStructures", "ManagementStatistics", "ComputerSimulation", "ComputerProgramming", "Forecasting" ]
right = [ "Student" ]
implications = {
    ( "DataStructures", "Student" ): ( ( "ComputerProgramming", "Student", 1 ), ),
    ( "ComputerSimulation", "Student" ): ( ( "ComputerProgramming", "Student", 1 ), ),
    ( "ManagementStatistics", "Student" ): ( ( "Calculus", "Student", 1 ), ),
    ( "Forecasting", "Student" ): ( ( "ManagementStatistics", "Student", 1 ), ),
}


labels = [ "Mathematics", "ComputerScience", "OperationsResearch" ]
val = {
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

max_capacities = {
    ( "Calculus", "Student" ): 1,
    ( "OperationsResearch", "Student" ): 1,
    ( "DataStructures", "Student" ): 1,
    ( "ManagementStatistics", "Student" ): 1,
    ( "ComputerSimulation", "Student" ): 1,
    ( "ComputerProgramming", "Student" ): 1,
    ( "Forecasting", "Student" ): 1,
}

ressouces_config: RessourcesConfig = RessourcesConfig(
    labels=labels,
    vals=val,
    objectives=objectives,
    weights=weights,
    min_vals=min_val,
)

problem: AssignmentProblem = AssignmentProblem(
    left_labels=left,
    right_labels=right,
    use_ressources=True,
    ressources_config=ressouces_config,
    implications=implications,
    max_capacities=max_capacities,
)

test: ORToolsAssignmentSolver = ORToolsAssignmentSolver()

solutions = test.solve( problem )

print(solutions)
