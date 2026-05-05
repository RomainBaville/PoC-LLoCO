# SPDX-License-Identifier: Apache-2.0
from dataclasses import dataclass
from typing import Callable


@dataclass
class AssignmentVariant:
    key: str
    label: str
    description: str
    render_fn: Callable


ASSIGNMENT_VARIANTS = {
    "skills": AssignmentVariant(
        key="skills",
        label="Skill‑based assignment",
        description="Assign entities based on skill levels and requirements",
        render_fn="ui.problems.assignment.skills.ui.render",
    ),
}
