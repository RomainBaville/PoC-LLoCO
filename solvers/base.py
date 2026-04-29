# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from abc import ABC, abstractmethod


class Solver(ABC):
    """
    Abstract solver interface.
    """

    @abstractmethod
    def solve(self, problem):
        """
        Solve a domain problem / structure.
        Must return a serializable solution.
        """
        ...

