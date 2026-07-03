# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from domain.assignment.base import AssignmentProblem
from domain.assignment.constraints.constraints_config import ConstraintsConfig
from domain.assignment.score.ressources_config import RessourcesConfig
from domain.assignment.score.score_config import ScoreConfig
from domain.objective import Objective

"""Problem description:
A convenience supermarket is planning to open several chain stores in a newly built residential area in the northwest
suburb of the city. For shopping convenience, the distance from any residential area to one of the chain stores should
not exceed 800m. Table 5-1 shows the new residential areas and the residential areas within a radius of 800m from each
of them.

Question: What is the minimum number of chain stores the supermarket needs to build among the mentioned residential
areas, and in which residential areas should they be built?

| Area Code | Residential Areas within 800m Radius|
|-----------|-------------------------------------|
| A         | A, C, E, G, H, I                    |
| B         | B, H, I                             |
| C         | A, C, G, H, I                       |
| D         | D, J                                |
| E         | A, E, G                             |
| F         | F, J, K                             |
| G         | A, C, E, G                          |
| H         | A, B, C, H, I                       |
| I         | A, B, C, H, I                       |
| J         | D, F, J, K, L                       |
| K         | F, J, K, L                          |
| L         | J, K, L                             |
"""

left_labels: tuple[ str, ...] = ( "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L" )
right_labels: tuple[ str, ...] = ( "Commerces", )

# Score
labels: tuple[ str, ...] = (
    "A_800", "B_800", "C_800", "D_800", "E_800", "F_800", "G_800", "H_800", "I_800", "J_800", "K_800", "L_800"
)
vals: dict[ tuple[ str, str ], float ] = {
    ( "A", "A_800" ): 1.,
    ( "A", "B_800" ): 0.,
    ( "A", "C_800" ): 1.,
    ( "A", "D_800" ): 0.,
    ( "A", "E_800" ): 1.,
    ( "A", "F_800" ): 0.,
    ( "A", "G_800" ): 1.,
    ( "A", "H_800" ): 1.,
    ( "A", "I_800" ): 1.,
    ( "A", "J_800" ): 0.,
    ( "A", "K_800" ): 0.,
    ( "A", "L_800" ): 0.,
    ( "B", "A_800" ): 0.,
    ( "B", "B_800" ): 1.,
    ( "B", "C_800" ): 0.,
    ( "B", "D_800" ): 0.,
    ( "B", "E_800" ): 0.,
    ( "B", "F_800" ): 0.,
    ( "B", "G_800" ): 0.,
    ( "B", "H_800" ): 1.,
    ( "B", "I_800" ): 1.,
    ( "B", "J_800" ): 0.,
    ( "B", "K_800" ): 0.,
    ( "B", "L_800" ): 0.,
    ( "C", "A_800" ): 1.,
    ( "C", "B_800" ): 0.,
    ( "C", "C_800" ): 1.,
    ( "C", "D_800" ): 0.,
    ( "C", "E_800" ): 0.,
    ( "C", "F_800" ): 0.,
    ( "C", "G_800" ): 1.,
    ( "C", "H_800" ): 1.,
    ( "C", "I_800" ): 1.,
    ( "C", "J_800" ): 0.,
    ( "C", "K_800" ): 0.,
    ( "C", "L_800" ): 0.,
    ( "D", "A_800" ): 0.,
    ( "D", "B_800" ): 0.,
    ( "D", "C_800" ): 0.,
    ( "D", "D_800" ): 1.,
    ( "D", "E_800" ): 0.,
    ( "D", "F_800" ): 0.,
    ( "D", "G_800" ): 0.,
    ( "D", "H_800" ): 0.,
    ( "D", "I_800" ): 0.,
    ( "D", "J_800" ): 1.,
    ( "D", "K_800" ): 0.,
    ( "D", "L_800" ): 0.,
    ( "E", "A_800" ): 1.,
    ( "E", "B_800" ): 0.,
    ( "E", "C_800" ): 0.,
    ( "E", "D_800" ): 0.,
    ( "E", "E_800" ): 1.,
    ( "E", "F_800" ): 0.,
    ( "E", "G_800" ): 1.,
    ( "E", "H_800" ): 0.,
    ( "E", "I_800" ): 0.,
    ( "E", "J_800" ): 0.,
    ( "E", "K_800" ): 0.,
    ( "E", "L_800" ): 0.,
    ( "F", "A_800" ): 0.,
    ( "F", "B_800" ): 0.,
    ( "F", "C_800" ): 0.,
    ( "F", "D_800" ): 0.,
    ( "F", "E_800" ): 0.,
    ( "F", "F_800" ): 1.,
    ( "F", "G_800" ): 0.,
    ( "F", "H_800" ): 0.,
    ( "F", "I_800" ): 0.,
    ( "F", "J_800" ): 1.,
    ( "F", "K_800" ): 1.,
    ( "F", "L_800" ): 0.,
    ( "G", "A_800" ): 1.,
    ( "G", "B_800" ): 0.,
    ( "G", "C_800" ): 1.,
    ( "G", "D_800" ): 0.,
    ( "G", "E_800" ): 1.,
    ( "G", "F_800" ): 0.,
    ( "G", "G_800" ): 1.,
    ( "G", "H_800" ): 0.,
    ( "G", "I_800" ): 0.,
    ( "G", "J_800" ): 0.,
    ( "G", "K_800" ): 0.,
    ( "G", "L_800" ): 0.,
    ( "H", "A_800" ): 1.,
    ( "H", "B_800" ): 1.,
    ( "H", "C_800" ): 1.,
    ( "H", "D_800" ): 0.,
    ( "H", "E_800" ): 0.,
    ( "H", "F_800" ): 0.,
    ( "H", "G_800" ): 0.,
    ( "H", "H_800" ): 1.,
    ( "H", "I_800" ): 1.,
    ( "H", "J_800" ): 0.,
    ( "H", "K_800" ): 0.,
    ( "H", "L_800" ): 0.,
    ( "I", "A_800" ): 1.,
    ( "I", "B_800" ): 1.,
    ( "I", "C_800" ): 1.,
    ( "I", "D_800" ): 0.,
    ( "I", "E_800" ): 0.,
    ( "I", "F_800" ): 0.,
    ( "I", "G_800" ): 0.,
    ( "I", "H_800" ): 1.,
    ( "I", "I_800" ): 1.,
    ( "I", "J_800" ): 0.,
    ( "I", "K_800" ): 0.,
    ( "I", "L_800" ): 0.,
    ( "J", "A_800" ): 0.,
    ( "J", "B_800" ): 0.,
    ( "J", "C_800" ): 0.,
    ( "J", "D_800" ): 1.,
    ( "J", "E_800" ): 0.,
    ( "J", "F_800" ): 1.,
    ( "J", "G_800" ): 0.,
    ( "J", "H_800" ): 0.,
    ( "J", "I_800" ): 0.,
    ( "J", "J_800" ): 1.,
    ( "J", "K_800" ): 1.,
    ( "J", "L_800" ): 1.,
    ( "K", "A_800" ): 0.,
    ( "K", "B_800" ): 0.,
    ( "K", "C_800" ): 0.,
    ( "K", "D_800" ): 0.,
    ( "K", "E_800" ): 0.,
    ( "K", "F_800" ): 1.,
    ( "K", "G_800" ): 0.,
    ( "K", "H_800" ): 0.,
    ( "K", "I_800" ): 0.,
    ( "K", "J_800" ): 1.,
    ( "K", "K_800" ): 1.,
    ( "K", "L_800" ): 1.,
    ( "L", "A_800" ): 0.,
    ( "L", "B_800" ): 0.,
    ( "L", "C_800" ): 0.,
    ( "L", "D_800" ): 0.,
    ( "L", "E_800" ): 0.,
    ( "L", "F_800" ): 0.,
    ( "L", "G_800" ): 0.,
    ( "L", "H_800" ): 0.,
    ( "L", "I_800" ): 0.,
    ( "L", "J_800" ): 1.,
    ( "L", "K_800" ): 1.,
    ( "L", "L_800" ): 1.,
}
objectives: dict[ str, Objective ] = {
    "A_800": Objective.MINIMIZE,
    "B_800": Objective.MINIMIZE,
    "C_800": Objective.MINIMIZE,
    "D_800": Objective.MINIMIZE,
    "E_800": Objective.MINIMIZE,
    "F_800": Objective.MINIMIZE,
    "G_800": Objective.MINIMIZE,
    "H_800": Objective.MINIMIZE,
    "I_800": Objective.MINIMIZE,
    "J_800": Objective.MINIMIZE,
    "K_800": Objective.MINIMIZE,
    "L_800": Objective.MINIMIZE,
}
weights: dict[ str, float ] = {
    "A_800": 1.,
    "B_800": 1.,
    "C_800": 1.,
    "D_800": 1.,
    "E_800": 1.,
    "F_800": 1.,
    "G_800": 1.,
    "H_800": 1.,
    "I_800": 1.,
    "J_800": 1.,
    "K_800": 1.,
    "L_800": 1.,
}
min_vals: dict[ tuple[ str, ...], float ] = {
    ( "Commerces", "A_800" ): 1.,
    ( "Commerces", "B_800" ): 1.,
    ( "Commerces", "C_800" ): 1.,
    ( "Commerces", "D_800" ): 1.,
    ( "Commerces", "E_800" ): 1.,
    ( "Commerces", "F_800" ): 1.,
    ( "Commerces", "G_800" ): 1.,
    ( "Commerces", "H_800" ): 1.,
    ( "Commerces", "I_800" ): 1.,
    ( "Commerces", "J_800" ): 1.,
    ( "Commerces", "K_800" ): 1.,
    ( "Commerces", "L_800" ): 1.,
}

ressource_config: RessourcesConfig = RessourcesConfig(
    labels=labels,
    vals=vals,
    objectives=objectives,
    weights=weights,
    min_vals=min_vals,
)

score_config: ScoreConfig = ScoreConfig( use_ressources=True, ressources_config=ressource_config )

# constraints
constraints_config: ConstraintsConfig = ConstraintsConfig()

problem_10: AssignmentProblem = AssignmentProblem(
    left_labels=left_labels,
    right_labels=right_labels,
    score_config=score_config,
    constraints_config=constraints_config,
)
solution_10: dict[ list[ tuple[ str, int ] ] ] = {
    "B": [ ( "Commerces", 1 ) ],
    "G": [ ( "Commerces", 1 ) ],
    "J": [ ( "Commerces", 1 ) ],
}
