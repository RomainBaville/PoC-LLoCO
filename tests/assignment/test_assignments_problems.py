# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville
import pytest

import sys
from pathlib import Path

# --- make project root importable ---
ROOT_DIR = Path( __file__ ).resolve().parents[2]
sys.path.append( str( ROOT_DIR ) )

from domain.assignment.base import AssignmentProblem

from solvers.assignment.cp_model.ortools_cp_sat import solve_assignment_problem

from tests.assignment.problem_00.problem_00 import problem_00, solution_00
from tests.assignment.problem_08.problem_08 import problem_08, solution_08
from tests.assignment.problem_10.problem_10 import problem_10, solution_10
from tests.assignment.problem_19.problem_19 import problem_19, solution_19
from tests.assignment.problem_55.problem_55 import problem_55, solution_55
from tests.assignment.problem_84.problem_84 import problem_84, solution_84


@pytest.mark.parametrize( "problem, expected_solution", [
    ( problem_00, solution_00 ),
    ( problem_08, solution_08 ),
    ( problem_10, solution_10 ),
    ( problem_19, solution_19 ),
    ( problem_55, solution_55 ),
    ( problem_84, solution_84 ),
] )
def test_assignments_problem(
    problem: AssignmentProblem,
    expected_solution: dict[ str, list[ tuple[ str, int ] ] ] ) -> None:
    """Test the resolution of assignments problems of the IndustryOR.json file."""
    obtained_solution: dict[ str, list[ tuple[ str, int ] ] ] = solve_assignment_problem( problem )
    assert obtained_solution == expected_solution
