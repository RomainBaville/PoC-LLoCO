# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from dataclasses import dataclass
from typing_extensions import Callable

from ui.assignment.ui_assignment import render


@dataclass
class ProblemType:
    key: str
    label: str
    description: str
    render_fn: Callable


PROBLEM_REGISTRY: dict[ str, ProblemType ] = {
    "assignment": ProblemType(
        key="assignment",
        label="Assignment problem",
        description="Assignments problem between left and right entities",
        render_fn=render,
    ),
}
