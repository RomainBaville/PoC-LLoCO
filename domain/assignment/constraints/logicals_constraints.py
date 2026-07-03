# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from dataclasses import dataclass


@dataclass
class LogicalsConstraints:
    """Dataclass to configure the logicals constraints of the assignment problem.

    Args:
        left_mutual_exclusions (Optional[tuple[tuple[str, ...], ...]]):
            Groups of left entity labels that can't be associated together.
        right_mutual_exclusions (Optional[tuple[tuple[str, ...], ...]]):
            Groups of right entity labels that can't be assigned together.
        implications (Optional[dict[tuple[str, str], tuple[tuple[str, str, Optional[float]], ...]]]):
            The dictionary with the implication of an association:
            - keys (tuple[str, str]): The left and right entity labels of the association with an implication.
            - values (tuple[tuple[str, str, float], ...]]): The left and rigth labels of the implicated association
                with the number of forced associations.
    """
    left_mutual_exclusions: tuple[ tuple[ str, ...], ...] | None = None
    right_mutual_exclusions: tuple[ tuple[ str, ...], ...] | None = None
    implications: dict[ tuple[ str, str ], tuple[ tuple[ str, str, float ], ...] ] | None = None
