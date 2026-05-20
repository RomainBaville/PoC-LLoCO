# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.

from dataclasses import dataclass


@dataclass
class ProblemDefinition:
    key: str
    label: str


PROBLEM_REGISTRY = {
    "assignment": ProblemDefinition(
        key="assignment",
        label="Assignment problem",
    ),
}
