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

from tests.assignment.ok.problem_08.problem_08 import problem_08, solution_08
from tests.assignment.ok.problem_55.problem_55 import problem_55, solution_55

@pytest.mark.parametrize( "problem, expected_solution", [
    ( problem_08, solution_08 ),
    ( problem_55, solution_55 ),
] )
def test_assignments_problem(
    problem: AssignmentProblem,
    expected_solution: dict[ str, list[ tuple[ str, int ] ] ] ) -> None:
    """Test the resolution of assignments problems."""
    obtained_solution: dict[ str, list[ tuple[ str, int ] ] ] = solve_assignment_problem( problem )
    assert obtained_solution == expected_solution
