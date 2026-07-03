# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from domain.assignment.base import AssignmentProblem
from domain.assignment.constraints.constraints_config import ConstraintsConfig
from domain.assignment.constraints.logicals_constraints import LogicalsConstraints
from domain.assignment.constraints.quantities_constraints import QuantitiesConstraints
from domain.assignment.score.ressources_config import RessourcesConfig
from domain.assignment.score.score_config import ScoreConfig
from domain.objective import Objective
"""Problem description:
A company hopes to recruit new employees for its team. The salary requirements for candidates A, B, C, D, and E
are $8100, $20000, $21000, $3000, and $8000 respectively. They need to decide whether to hire each candidate.
The team wants to minimize the total amount paid to the candidates.

They hope to hire a maximum of 3 new employees.The team has a limited budget of $35,000.
They need to ensure that the total payment to the selected candidates does not exceed the budget.
The qualifications of the five candidates are as follows:
Candidate A: Bachelor's degree;
Candidate B: Master's degree;
Candidate C: Doctoral degree;
Candidate D: No degree;
Candidate E: No degree.
They will select at least one candidate with a Master's or Doctoral degree.
The work experience of the five candidates is as follows:
Candidate A: 3 years of work experience;
Candidate B: 10 years of work experience;
Candidate C: 4 years of work experience;
Candidate D: 3 years of work experience;
Candidate E: 7 years of work experience.
They hope the total work experience of the selected candidates is no less than 12 years.
Due to the equivalent professional skills of candidates A and E, the company will choose at most one from the two.
They will hire at least 2 new employees.
"""

left_labels: tuple[ str, ...] = ( "A", "B", "C", "D", "E" )
right_labels: tuple[ str, ...] = ( "Entreprise", )

# Score
labels: tuple[ str, ...] = ( "Salary", "Work_Experience_Years", "Degree_Level" )
vals: dict[ tuple[ str, str ], float ] = {
    ( "A", "Salary" ): 8100.,
    ( "A", "Work_Experience_Years" ): 3.,
    ( "A", "Degree_Level" ): 3.,
    ( "B", "Salary" ): 20000.,
    ( "B", "Work_Experience_Years" ): 10.,
    ( "B", "Degree_Level" ): 5.,
    ( "C", "Salary" ): 21000.,
    ( "C", "Work_Experience_Years" ): 4.,
    ( "C", "Degree_Level" ): 8.,
    ( "D", "Salary" ): 3000.,
    ( "D", "Work_Experience_Years" ): 3.,
    ( "D", "Degree_Level" ): 0.,
    ( "E", "Salary" ): 8000.,
    ( "E", "Work_Experience_Years" ): 7.,
    ( "E", "Degree_Level" ): 0.,
}
objectives: dict[ str, Objective ] = {
    "Salary": Objective.MINIMIZE,
    "Work_Experience_Years": Objective.MAXIMIZE,
    "Degree_Level": Objective.MAXIMIZE,
}
weights: dict[ str, float ] = {
    "Salary": 1.,
    "Work_Experience_Years": 1.,
    "Degree_Level": 1.,
}

max_vals: dict[ tuple[ str, ...], float ] = {
    ( "Entreprise", "Salary" ): 35000.,
}
min_vals: dict[ tuple[ str, ...], float ] = {
    ( "Entreprise", "Degree_Level" ): 5.,
    ( "Entreprise", "Work_Experience_Years" ): 12.,
}

ressources_config: RessourcesConfig = RessourcesConfig(
    labels=labels,
    vals=vals,
    objectives=objectives,
    weights=weights,
    max_vals=max_vals,
    min_vals=min_vals,
)

score_config: ScoreConfig = ScoreConfig(
    use_ressources=True,
    ressources_config=ressources_config,
)

# Constraints
max_left_entities: dict[ str, float ] = {
    "Entreprise": 3.,
}
min_left_entities: dict[ str, float ] = {
    "Entreprise": 2.,
}

quantities_constraints: QuantitiesConstraints = QuantitiesConstraints(
    max_left_entities=max_left_entities,
    min_left_entities=min_left_entities,
)

left_mutual_exclusions: tuple[ tuple[ str, str ], ...] = ( ( "A", "E" ), )

logicals_constraints: LogicalsConstraints = LogicalsConstraints( left_mutual_exclusions=left_mutual_exclusions, )

constraints_config: ConstraintsConfig = ConstraintsConfig(
    use_logicals_constraints=True,
    logicals_constraints=logicals_constraints,
    use_quantities_constraints=True,
    quantities_constraints=quantities_constraints,
)

problem_84_domain: AssignmentProblem = AssignmentProblem(
    left_labels=left_labels,
    right_labels=right_labels,
    score_config=score_config,
    constraints_config=constraints_config,
)
solution_84: dict[ str, list[ tuple[ str, int ] ] ] = {
    "B": [
        ( "Entreprise", 1 ),
    ],
    "D": [
        ( "Entreprise", 1 ),
    ],
}
