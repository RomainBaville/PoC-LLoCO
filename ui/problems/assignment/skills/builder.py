# SPDX-License-Identifier: Apache-2.0
from domain.assignment.skills import SkillBasedAssignmentProblem


def build_problem(state, left_rows, right_rows):

    left_entities = []
    right_entities = []
    left_skills = {}
    right_requirements = {}

    for row in left_rows:
        l = " ".join(row[c] for c in state.left_id_cols)
        left_entities.append(l)
        for s in state.skill_cols:
            left_skills[(l, s)] = int(row.get(s, 0))

    for row in right_rows:
        r = row[state.right_id_col]
        right_entities.append(r)
        for s in state.skill_cols:
            right_requirements[(r, s)] = int(row.get(s, 0))

    return SkillBasedAssignmentProblem(
        left_entities=left_entities,
        right_entities=right_entities,
        skills=state.skill_cols,
        left_skills=left_skills,
        right_requirements=right_requirements,
    )
