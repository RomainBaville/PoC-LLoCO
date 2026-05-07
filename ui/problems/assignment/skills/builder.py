# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from domain.assignment.skills import SkillBasedAssignmentProblem
from domain.entity_registry import EntityRegistry


def build_problem(state, left_rows, right_rows):

    left_registry = EntityRegistry(prefix="left")

    left_entities = []
    right_entities = []
    left_skills = {}
    right_requirements = {}

    # ---------------------------------------------
    # Left entities (internal IDs + labels)
    # ---------------------------------------------
    for row in left_rows:
        label = " ".join(row[c] for c in state.left_id_cols)
        left_id = left_registry.create(label)

        left_entities.append(left_id)

        for skill in state.skill_cols:
            left_skills[(left_id, skill)] = int(row.get(skill, 0))

    # ---------------------------------------------
    # Right entities (IDs are already unique by CSV column)
    # ---------------------------------------------
    for row in right_rows:
        right_id = row[state.right_id_col]
        right_entities.append(right_id)

        for skill in state.skill_cols:
            right_requirements[(right_id, skill)] = int(row.get(skill, 0))

    problem = SkillBasedAssignmentProblem(
        left_entities=left_entities,
        right_entities=right_entities,
        skills=state.skill_cols,
        left_skills=left_skills,
        right_requirements=right_requirements,
    )

    return problem, left_registry.labels
