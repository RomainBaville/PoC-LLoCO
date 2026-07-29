# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville
import sys
from pathlib import Path

import pytest

from domain.assignment.base import AssignmentProblem
from solvers.assignment.cp_model.ortools_cp_sat import solve_assignment_problem
from tests.assignment.problem_08.problem_08_description import problem_08_domain, solution_08
from tests.assignment.problem_10.problem_10_description import problem_10_domain, solution_10
from tests.assignment.problem_19.problem_19_description import problem_19_domain, solution_19
from tests.assignment.problem_55.problem_55_description import problem_55_domain, solution_55
from tests.assignment.problem_84.problem_84_description import problem_84_domain, solution_84

# --- make project root importable ---
ROOT_DIR = Path( __file__ ).resolve().parents[ 2 ]
sys.path.append( str( ROOT_DIR ) )


@pytest.mark.parametrize(
    "problem, expected_solution",
    [
        ( problem_08_domain, solution_08 ),
        ( problem_10_domain, solution_10 ),
        ( problem_19_domain, solution_19 ),
        ( problem_55_domain, solution_55 ),
        ( problem_84_domain, solution_84 ),
    ]
)
def test_assignments_problem_unique(
    problem: AssignmentProblem,
    expected_solution: dict[ str, list[ tuple[ str, int ] ] ],
) -> None:
    """Test the resolution of assignments problems of the IndustryOR.json file.

    All the problem tested here have a unique solution

    Args:
        problem (AssignmentProblem): The assignment problem.
        expected_solution (dict[str, list[tuple[str, int]]]): The expected solution.
    """
    obtained_solution: dict[ str, list[ tuple[ str, int ] ] ] = solve_assignment_problem( problem )
    assert obtained_solution == expected_solution

# TODO: test problem with none unique solution starting with problem 0
