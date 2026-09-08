# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from dataclasses import dataclass, field

from typing_extensions import Any


@dataclass
class OptimizationSession:
    """Structured representation of a complete optimization run passed to the LLM prompt builder."""
    journey: dict[ str, Any ] = field(
        metadata={
            "description": "All the data set in the interface trought the problem resolution."
        }
    )
    result: Any = field( metadata={
        "description": "The result of the optimization resolution."
    } )
    user_desc: str | None = field(
        default=None, metadata={
            "description": "The problem description set by the user."
        }
    )
    onboarding: str | None = field( default=None, metadata={
        "description": "The AI onbording text."
    } )
