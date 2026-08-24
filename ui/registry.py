# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.

from collections.abc import Callable
from dataclasses import dataclass

from streamlit.runtime.state.session_state_proxy import SessionStateProxy

from ui.assignment.ui_assignment import render


@dataclass
class ProblemType:
    """Dataclass to acces to all the type of problems the user interface can deals with.

    Args:
        key (str): The key of the problem.
        label (str): The label of the problem.
        description (str): A short description of the problem.
        render_fn (Callable[[SessionStateProxy], None]): The function with the ui for this type of problem.
    """
    key: str
    label: str
    description: str
    render_fn: Callable[ [ SessionStateProxy ], None ]


PROBLEM_REGISTRY: dict[ str, ProblemType ] = {
    "assignment":
    ProblemType(
        key="assignment",
        label="Assignment problem",
        description="Assignments problem between left and right entities",
        render_fn=render,
    ),
}
