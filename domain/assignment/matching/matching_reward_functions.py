# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

import math
from enum import Enum
from typing_extensions import Self, Callable


def score_min( left_val: float, right_val: float ) -> float:
    return min( left_val, right_val )


def score_product( left_val: float, right_val: float ) -> float:
    return left_val * right_val


def score_ratio( left_val: float, right_val: float ) -> float:
    if right_val == 0:
        return 0.
    return min( left_val / right_val, 1 )


def score_threshold( left_val: float, right_val: float ) -> float:
    return 1. if left_val >= right_val else 0.


def score_sqrt_product( left_val: float, right_val: float ) -> float:
    return math.sqrt( left_val * right_val )


def score_log_product( left_val: float, right_val: float ) -> float:
    return math.log( 1 + left_val * right_val )


def score_soft_min( left_val: float, right_val: float ) -> float:
    return ( left_val * right_val ) / ( left_val + right_val + 1e-6 )


class RewardFunctions( Enum ):
    """Enum for reward functions."""
    MIN: Callable[ [ float, float ], float ] = ( score_min, )
    PRODUCT: Callable[ [ float, float ], float ] = ( score_product, )
    RATIO: Callable[ [ float, float ], float ] = ( score_ratio, )
    THRESHOLD: Callable[ [ float, float ], float ] = ( score_threshold, )
    SQRT_PRODUCT: Callable[ [ float, float ], float ] = ( score_sqrt_product, )
    LOG_PRODUC: Callable[ [ float, float ], float ] = ( score_log_product, )
    SOFT_MIN: Callable[ [ float, float ], float ] = ( score_soft_min, )

    def __init__( self: Self, func ):
        self.func = func

    def __str__( self: Self ) -> str:
        return self.name

    def __call__( self: Self, left_val: float, right_val: float ) -> float:
        return self.func( left_val, right_val )
