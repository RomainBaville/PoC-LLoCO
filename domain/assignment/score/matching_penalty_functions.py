# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

import math
from collections.abc import Callable
from enum import Enum
from typing import Self


def no_penalty( left_val: float, right_val: float ) -> float:
    return 0.


def score_shortfall( left_val: float, right_val: float ) -> float:
    return -max( 0., right_val - left_val )


def score_absdiff( left_val: float, right_val: float ) -> float:
    return -abs( left_val - right_val )


def score_relative_shortfall( left_val: float, right_val: float ) -> float:
    if right_val == 0:
        return 0.
    return -max( 0., ( right_val - left_val ) / right_val )


def score_squared_diff( left_val: float, right_val: float ) -> float:
    return -( left_val - right_val )**2


def score_shortfall_squared( left_val: float, right_val: float ) -> float:
    return -( max( 0., right_val - left_val )**2 )


def score_overqualification( left_val: float, right_val: float ) -> float:
    return -max( 0., left_val - right_val )


def score_log_shortfall( left_val: float, right_val: float ) -> float:
    return -math.log( 1. + max( 0., right_val - left_val ) )


class PenaltyFunctions( Enum ):
    """Enum for penalty functions."""
    NONE: Callable[ [ float, float ], float ] = ( no_penalty, )
    SHORTFALL: Callable[ [ float, float ], float ] = ( score_shortfall, )
    ABS_DIFF: Callable[ [ float, float ], float ] = ( score_absdiff, )
    RELATIVE_SHORTFALL: Callable[ [ float, float ], float ] = ( score_relative_shortfall, )
    SQUARED_DIFF: Callable[ [ float, float ], float ] = ( score_squared_diff, )
    SHORTFALL_SQUARED: Callable[ [ float, float ], float ] = ( score_shortfall_squared, )
    OVERQUALIFICATION: Callable[ [ float, float ], float ] = ( score_overqualification, )
    LOG_SHORTFALL: Callable[ [ float, float ], float ] = ( score_log_shortfall, )

    def __init__( self: Self, func ):
        self.func = func

    def __str__( self: Self ) -> str:
        return self.name

    def __call__( self: Self, left_val: float, right_val: float ) -> float:
        return self.func( left_val, right_val )
