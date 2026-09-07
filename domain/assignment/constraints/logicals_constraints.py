# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from dataclasses import dataclass, field


@dataclass
class LogicalsConstraints:
    """Configure logical assignment constraints."""

    left_mutual_exclusions: tuple[ tuple[ str, ...], ...] | None = field(
        default=None, metadata={
            "description": "Groups of left entities that cannot be assigned together."
        }
    )

    right_mutual_exclusions: tuple[ tuple[ str, ...], ...] | None = field(
        default=None, metadata={
            "description": "Groups of right entities that cannot be assigned together."
        }
    )

    implications: ( dict[
        tuple[ str, str ],
        tuple[ tuple[ str, str, float ], ...],
    ] | None ) = field(
        default=None, metadata={
            "description": "Assignment implications triggered by another assignment."
        }
    )
