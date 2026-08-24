# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from dataclasses import dataclass


@dataclass
class QuantitiesConstraints:
    """Dataclass to configure the quantities constraints of the assignment problem.

    Args:
        max_right_entities (Optional[dict[str, float]]):
            The dictionary with the maximum number of different right entities, a left entity can be assigned to:
            - keys (str): The left entity label.
            - values (float): The maximum number of different right entities allowed.
        min_right_entities (Optional[dict[str, float]]):
            The dictionary with the minimum number of different right entities, a left entity can be assigned to:
            - keys (str): The left entity label.
            - values (float): The minimum number of different right entities allowed.
        max_left_entities (Optional[dict[str, float]]):
            The dictionary with the maximum number of different left entities, a right entity can handled:
            - keys (str): The right entity label.
            - values (float): The maximum number of different left entities allowed.
        min_left_entities (Optional[dict[str, float]]):
            The dictionary with the minimum number of different left entities, a right entity can handled:
            - keys (str): The right entity label.
            - values (float): The minimum number of different left entities allowed.
        max_same_assignments (Optional[dict[tuple[str, str], float]]):
            The dictionary whit the maximum number of assignments allowed by left entities per right entities:
            - keys (tuple[str, str]): The left and right entity labels.
            - value (float): The maximum number of assignments allowed by the left entity for the right entity.
        min_same_assignments (Optional[dict[tuple[str, str], float]]):
            The dictionary whit the minimum number of assignments allowed by left entities per right entities:
            - keys (tuple[str, str]): The left and right entity labels.
            - value (float): The minimum number of assignments allowed by the left entity for the right entity.
        max_right_assignments (Optional[dict[str, float]]):
            The dictionary whit the maximum number of assignments allowed per left entities:
            - keys (str): The left entity label.
            - value (float): The maximum number of assignments allowed for the left entity.
        min_right_assignments (Optional[dict[str, float]]):
            The dictionary whit the minimum number of assignments allowed per left entities:
            - keys (str): The left entity label.
            - value (float): The minimum number of assignments allowed for the left entity.
        max_left_assignments (Optional[dict[str, float]]):
            The dictionary whit the maximum number of assignments allowed per right entities:
            - keys (str): The right entity label.
            - value (float): The maximum number of assignments allowed for the right entity.
        min_left_assignments (Optional[dict[str, float]]):
            The dictionary whit the minimum number of assignments allowed per right entities:
            - keys (str): The right entity label.
            - value (float): The minimum number of assignments allowed for the right entity.
    """
    max_right_entities: dict[ str, float ] | None = None
    min_right_entities: dict[ str, float ] | None = None

    max_left_entities: dict[ str, float ] | None = None
    min_left_entities: dict[ str, float ] | None = None

    # To configure if multiple_same_assignment is True
    max_same_assignments: dict[ tuple[ str, str ], float ] | None = None
    min_same_assignments: dict[ tuple[ str, str ], float ] | None = None

    max_right_assignments: dict[ str, float ] | None = None
    min_right_assignments: dict[ str, float ] | None = None

    max_left_assignments: dict[ str, float ] | None = None
    min_left_assignments: dict[ str, float ] | None = None
