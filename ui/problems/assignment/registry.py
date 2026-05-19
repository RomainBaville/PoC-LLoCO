# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from dataclasses import dataclass


@dataclass
class AssignmentType:
    key: str
    label: str
    description: str
    registry_module: str   # import path to type registry


ASSIGNMENT_TYPES = {
    "skills": AssignmentType(
        key="skills",
        label="Skill-based assignment",
        description="Assignments driven by skills, competencies or qualifications",
        registry_module="ui.problems.assignment.skills.registry",
    ),

    # Future example:
    # "cost": AssignmentType(
    #     key="cost",
    #     label="Cost-based assignment",
    #     description="Assignments that minimize or balance cost",
    #     registry_module="ui.problems.assignment.cost.registry",
    # ),
}
