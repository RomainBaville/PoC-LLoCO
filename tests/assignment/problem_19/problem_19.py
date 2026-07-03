# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from domain.assignment.base import AssignmentProblem
from domain.assignment.constraints.constraints_config import ConstraintsConfig
from domain.assignment.constraints.logicals_constraints import LogicalsConstraints
from domain.assignment.score.ressources_config import RessourcesConfig
from domain.assignment.score.score_config import ScoreConfig
from domain.objective import Objective

"""Problem description:
A furniture store can choose to order chairs from three different manufacturers: A, B, and C. The cost of ordering each
chair from manufacturer A is $50, from manufacturer B is $45, and from manufacturer C is $40. The store needs to
minimize the total cost of the order.

Additionally, each order from manufacturer A will include 15 chairs, while each order from manufacturers B and C will
include 10 chairs. The number of orders must be an integer. The store needs to order at least 100 chairs and at most
500 chairs.

If the store decides to order chairs from manufacturer A, it must also order at least 10 chairs from manufacturer B.

Furthermore, if the store decides to order chairs from manufacturer B, it must also order chairs from manufacturer C.
"""

left_labels: tuple[ str, ...] = ( "A", "B", "C" )
right_labels: tuple[ str, ...] = ( "store", )

# Score
labels: tuple[ str, ...] = ( "Cost", "ChairsNumber" )
vals: dict[ tuple[ str, str ], float ] = {
    ( "A", "Cost" ): 750.,
    ( "A", "ChairsNumber" ): 15.,
    ( "B", "Cost" ): 450.,
    ( "B", "ChairsNumber" ): 10.,
    ( "C", "Cost" ): 400.,
    ( "C", "ChairsNumber" ): 10.,
}
objectives: dict[ str, Objective ] = {
    "Cost": Objective.MINIMIZE,
    "ChairsNumber": Objective.MAXIMIZE,
}
weights: dict[ str, float ] = {
    "Cost": 1.,
    "ChairsNumber": 1.,
}
max_vals: dict[ tuple[ str, ...], float ] = { ( "store", "ChairsNumber" ): 500. }
min_vals: dict[ tuple[ str, ...], float ] = { ( "store", "ChairsNumber" ): 100. }

ressouces_config: RessourcesConfig = RessourcesConfig(
    labels=labels,
    vals=vals,
    objectives=objectives,
    weights=weights,
    max_vals=max_vals,
    min_vals=min_vals,
)

score_config: ScoreConfig = ScoreConfig(
    use_ressources=True,
    ressources_config=ressouces_config,
)

# Constraints
implications: dict[ tuple[ str, str ], tuple[ tuple[ str, str, float ], ...] ] = {
    ( "A", "store" ): ( ( "B", "store", 1. ), ),
    ( "B", "store" ): ( ( "C", "store", 1. ), ),
}

logicals_constraints: LogicalsConstraints = LogicalsConstraints( implications=implications, )

constraints_config: ConstraintsConfig = ConstraintsConfig(
    use_logicals_constraints=True,
    logicals_constraints=logicals_constraints,
)

problem_19: AssignmentProblem = AssignmentProblem(
    left_labels=left_labels,
    right_labels=right_labels,
    score_config=score_config,
    constraints_config=constraints_config,
)
solution_19: dict[ str, list[ tuple[ str, int ] ] ] = { "C": [ ( "store", 10 ) ] }
