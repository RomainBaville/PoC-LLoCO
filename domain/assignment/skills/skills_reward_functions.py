# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

import math
from enum import Enum
from typing_extensions import Self, Callable


# Reward
def score_min( left: float, right: float ) -> float:
    return min( left, right )


def score_product( left: float, right: float ) -> float:
    return left * right


def score_ratio( left: float, right: float ) -> float:
    if right == 0:
        return 0
    return min( left / right, 1 )


def score_threshold( left: float, right: float ) -> float:
    return 1 if left >= right else 0


def score_sqrt_product( left: float, right: float ) -> float:
    return math.sqrt( left * right )


def score_log_product( left: float, right: float ) -> float:
    return math.log( 1 + left * right )


def score_soft_min( left: float, right: float ) -> float:
    return ( left * right ) / ( left + right + 1e-6 )


class RewardFunction( Enum ):
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

    def __call__( self: Self, left: float, right: float ) -> float:
        return self.func( left, right )
