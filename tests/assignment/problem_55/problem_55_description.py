# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from domain.assignment.base import AssignmentProblem
from domain.assignment.constraints.constraints_config import ConstraintsConfig
from domain.assignment.constraints.logicals_constraints import LogicalsConstraints
from domain.assignment.score.ressources_config import RessourcesConfig
from domain.assignment.score.score_config import ScoreConfig
from domain.objective import Objective

problem_55_prompt: str = (
    "A master's student in Operations Research at a certain university is required to select two courses in "
    "mathematics, two in operations research, and two in computer science from a total of seven courses: Calculus, "
    "Operations Research, Data Structures, Management Statistics, Computer Simulation, Computer Programming, and "
    "Forecasting. Some courses belong to only one category: Calculus falls under Mathematics, Computer Programming "
    "under Computer Science. However, some courses fall under multiple categories: Operations Research can be "
    "considered both Operations Research and Mathematics, Data Structures both Computer Science and Mathematics, "
    "Management Statistics both Mathematics and Operations Research, Computer Simulation both Computer Science and "
    "Operations Research, and Forecasting both Operations Research and Mathematics. Courses that fall under multiple "
    "categories can fulfill the requirement of both categories simultaneously. Additionally, some courses have "
    "prerequisites: Computer Simulation or Data Structures requires Computer Programming first, Management Statistics "
    "requires Calculus first, and Forecasting requires Management Statistics first. The question is: What is the "
    "minimum number of courses a master's student must take, and which specific courses, to meet the above "
    "requirements?"
)

# Problem
left_labels: tuple[ str, ...] = (
    "Calculus",
    "OperationsResearch",
    "DataStructures",
    "ManagementStatistics",
    "ComputerSimulation",
    "ComputerProgramming",
    "Forecasting"
)
right_labels: tuple[ str, ...] = ( "Student", )

# Score
labels: tuple[ str, ...] = ( "Mathematics", "ComputerScience", "OperationsResearch" )
vals: dict[ tuple[ str, str ], float ] = {
    ( "Calculus", "Mathematics" ): 1.,
    ( "Calculus", "ComputerScience" ): 0.,
    ( "Calculus", "OperationsResearch" ): 0.,
    ( "OperationsResearch", "Mathematics" ): 1.,
    ( "OperationsResearch", "ComputerScience" ): 0.,
    ( "OperationsResearch", "OperationsResearch" ): 1.,
    ( "DataStructures", "Mathematics" ): 1.,
    ( "DataStructures", "ComputerScience" ): 1.,
    ( "DataStructures", "OperationsResearch" ): 0.,
    ( "ManagementStatistics", "Mathematics" ): 1.,
    ( "ManagementStatistics", "ComputerScience" ): 0.,
    ( "ManagementStatistics", "OperationsResearch" ): 1.,
    ( "ComputerSimulation", "Mathematics" ): 0.,
    ( "ComputerSimulation", "ComputerScience" ): 1.,
    ( "ComputerSimulation", "OperationsResearch" ): 1.,
    ( "ComputerProgramming", "Mathematics" ): 0.,
    ( "ComputerProgramming", "ComputerScience" ): 1.,
    ( "ComputerProgramming", "OperationsResearch" ): 0.,
    ( "Forecasting", "Mathematics" ): 1.,
    ( "Forecasting", "ComputerScience" ): 0.,
    ( "Forecasting", "OperationsResearch" ): 1.
}
objectives: dict[ str, Objective ] = {
    "Mathematics": Objective.MINIMIZE,
    "ComputerScience": Objective.MINIMIZE,
    "OperationsResearch": Objective.MINIMIZE
}
weights: dict[ str, float ] = {
    "Mathematics": 1.,
    "ComputerScience": 1.,
    "OperationsResearch": 1.
}
min_val: dict[ tuple[ str, ...], float ] = {
    ( "Student", "Mathematics" ): 2.,
    ( "Student", "ComputerScience" ): 2.,
    ( "Student", "OperationsResearch" ): 2.
}

ressouces_config: RessourcesConfig = RessourcesConfig(
    labels=labels, vals=vals, objectives=objectives, weights=weights, min_vals=min_val
)

score_config: ScoreConfig = ScoreConfig( use_ressources=True, ressources_config=ressouces_config )

# Constraints
implications: dict[ tuple[ str, str ], tuple[ tuple[ str, str, float ], ...] ] = {
    ( "DataStructures", "Student" ): ( ( "ComputerProgramming", "Student", 1. ), ),
    ( "ComputerSimulation", "Student" ): ( ( "ComputerProgramming", "Student", 1. ), ),
    ( "ManagementStatistics", "Student" ): ( ( "Calculus", "Student", 1. ), ),
    ( "Forecasting", "Student" ): ( ( "ManagementStatistics", "Student", 1. ), )
}

logicals_constraints: LogicalsConstraints = LogicalsConstraints( implications=implications )

constraints_config: ConstraintsConfig = ConstraintsConfig(
    multiple_same_assignment=False, use_logicals_constraints=True, logicals_constraints=logicals_constraints
)

problem_55_domain: AssignmentProblem = AssignmentProblem(
    left_labels=left_labels,
    right_labels=right_labels,
    score_config=score_config,
    constraints_config=constraints_config
)

solution_55: dict[ str, list[ tuple[ str, int ] ] ] = {
    "Calculus": [ ( "Student", 1 ) ],
    "OperationsResearch": [ ( "Student", 1 ) ],
    "ComputerSimulation": [ ( "Student", 1 ) ],
    "ComputerProgramming": [ ( "Student", 1 ) ]
}
