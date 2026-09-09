# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from dataclasses import dataclass, field


@dataclass
class QuantitiesConstraints:
    """Configure quantity constraints of the assignment problem."""

    max_right_entities: dict[ str, float ] | None = field(
        default=None,
        metadata={
            "description": "Maximum number of different right entities a left entity can be assigned to."
        }
    )

    min_right_entities: dict[ str, float ] | None = field(
        default=None,
        metadata={
            "description": "Minimum number of different right entities a left entity can be assigned to."
        }
    )

    max_left_entities: dict[ str, float ] | None = field(
        default=None,
        metadata={
            "description": "Maximum number of different left entities a right entity can handle."
        }
    )

    min_left_entities: dict[ str, float ] | None = field(
        default=None,
        metadata={
            "description": "Minimum number of different left entities a right entity can handle."
        }
    )

    # To configure if multiple_same_assignment is True
    max_same_assignments: dict[ tuple[ str, str ], float ] | None = field(
        default=None,
        metadata={
            "description": "Maximum number of assignments allowed by a left entity for a right entity."
        }
    )

    min_same_assignments: dict[ tuple[ str, str ], float ] | None = field(
        default=None,
        metadata={
            "description": "Minimum number of assignments allowed by a left entity for a right entity."
        }
    )

    max_right_assignments: dict[ str, float ] | None = field(
        default=None, metadata={
            "description": "Maximum number of assignments allowed for a left entity."
        }
    )

    min_right_assignments: dict[ str, float ] | None = field(
        default=None, metadata={
            "description": "Minimum number of assignments allowed for a left entity."
        }
    )

    max_left_assignments: dict[ str, float ] | None = field(
        default=None, metadata={
            "description": "Maximum number of assignments allowed for a right entity."
        }
    )

    min_left_assignments: dict[ str, float ] | None = field(
        default=None, metadata={
            "description": ( "Minimum number of assignments allowed for a right entity." )
        }
    )
