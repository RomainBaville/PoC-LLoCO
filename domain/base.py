# SPDX-License-Identifier: Apache-2.0
from abc import ABC, abstractmethod


class DomainProblem(ABC):
    """
    Base class for any structured optimization problem.
    """

    @abstractmethod
    def validate(self):
        ...
