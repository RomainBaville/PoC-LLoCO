# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from dataclasses import dataclass
from typing import Callable, Type

from domain.assignment.skills.generic import SkillAssignmentProblem
from domain.assignment.config import AssignmentModelConfig


@dataclass
class AssignmentModel:
    """
    Definition of a configurable assignment model.

    There is only ONE model per assignment type.
    All behavior is controlled through config.
    """
    key: str
    label: str
    description: str
    render_fn: str
    domain_class: Type
    builder_fn: Callable


# --------------------------------------------------
# GENERIC ASSIGNMENT BUILDER
# --------------------------------------------------

def build_assignment(data):
    """
    Build a generic skill-based assignment problem.

    Behavior (coverage, best-fit, hybrid, constraints)
    is configured later via UI → config.
    """
    config = AssignmentModelConfig()

    problem = SkillAssignmentProblem(
        left_entities=data["left_entities"],
        right_entities=data["right_entities"],
        skills=data["skills"],
        left_skills=data["left_skills"],
        right_requirements=data["right_requirements"],
        config=config,
    )

    problem.validate()

    return problem


# --------------------------------------------------
# SINGLE MODEL ENTRY POINT
# --------------------------------------------------

ASSIGNMENT_MODEL = AssignmentModel(
    key="skills_assignment",
    label="Skill-based assignment",
    description=(
        "Assign entities based on skills with configurable behavior: "
        "matching quality, requirement satisfaction, and constraints."
    ),
    render_fn="ui.problems.assignment.skills.ui_skills.render",
    domain_class=SkillAssignmentProblem,
    builder_fn=build_assignment,
)
