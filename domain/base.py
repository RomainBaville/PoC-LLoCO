# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from abc import ABC, abstractmethod


class DomainProblem(ABC):
    """
    Base class for any structured optimization problem.
    """

    @abstractmethod
    def validate(self):
        ...
