# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from dataclasses import dataclass
from ui.problems.assignment_ui import render_assignment_step


@dataclass
class ProblemDefinition:
    key: str
    label: str
    render_fn: callable


PROBLEM_REGISTRY = {
    "assignment": ProblemDefinition(
        key="assignment",
        label="Assignment problem",
        render_fn=render_assignment_step,
    ),

    # Future:
    # "knapsack": ProblemDefinition(...)
}
