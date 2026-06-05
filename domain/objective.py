# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from enum import Enum

class Objective( Enum ):
    """Enum for objective functions."""
    MAXIMIZE = 1
    MINIMIZE = -1
