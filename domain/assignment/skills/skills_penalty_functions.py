# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

import math
from enum import Enum
from typing_extensions import Self, Callable

def no_penalty( left: float, right: float ) -> float:
    return 0


def score_shortfall( left: float, right: float ) -> float:
    return -max( 0, right - left )


def score_absdiff( left: float, right: float ) -> float:
    return -abs( left - right )


def score_relative_shortfall( left: float, right: float ) -> float:
    if right == 0:
        return 0
    return -max( 0, ( right - left ) / right )


def score_squared_diff( left: float, right: float ) -> float:
    return -( left - right ) ** 2


def score_shortfall_squared( left: float, right: float ) -> float:
    return -( max( 0, right - left ) ** 2 )


def score_overqualification( left: float, right: float ) -> float:
    return -max( 0, left - right )


def score_log_shortfall( left: float, right: float ) -> float:
    return -math.log( 1 + max( 0, right - left ) )


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

    def __call__( self: Self, left: float, right: float ) -> float:
        return self.func( left, right )
