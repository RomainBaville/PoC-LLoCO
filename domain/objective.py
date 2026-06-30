# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from enum import Enum
from typing import Self


class Objective( Enum ):
    """Enum for objective functions."""
    MAXIMIZE: int = 1
    MINIMIZE: int = -1

    def __str__( self: Self ) -> str:
        return self.name
