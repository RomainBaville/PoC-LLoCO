# SPDX-License-Identifier: Apache-2.0
from dataclasses import dataclass
from ui.problems.assignment.ui_router import render_assignment


@dataclass
class ProblemDefinition:
    key: str
    label: str
    render_fn: callable


PROBLEM_REGISTRY = {
    "assignment": ProblemDefinition(
        key="assignment",
        label="Assignment problem",
        render_fn=render_assignment,
    ),
}
