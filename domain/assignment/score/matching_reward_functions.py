# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

import math
from collections.abc import Callable
from enum import Enum
from typing import Self


def score_min( left_val: float, right_val: float ) -> float:
    """Get the min value between the left and the right values.

    Args:
        left_val (float): The value of the left entity variable.
        right_val (float): The value of the right entity variable.

    Returns:
        float: The min value between the two values.
    """
    return min( left_val, right_val )


def score_product( left_val: float, right_val: float ) -> float:
    """Get the product of the left and the right values.

    Args:
        left_val (float): The value of the left entity variable.
        right_val (float): The value of the right entity variable.

    Returns:
        float: The product of the two values.
    """
    return left_val * right_val


def score_ratio( left_val: float, right_val: float ) -> float:
    """Get the ratio between the left and the right values.

    Args:
        left_val (float): The value of the left entity variable.
        right_val (float): The value of the right entity variable.

    Returns:
        float: The ratio between the two values.
    """
    if right_val == 0:
        return 0.
    return min( left_val / right_val, 1 )


def score_threshold( left_val: float, right_val: float ) -> float:
    """Compare the left and the right values.

    Args:
        left_val (float): The value of the left entity variable.
        right_val (float): The value of the right entity variable.

    Returns:
        float: 1. if the left value is higher than the right. 0. otherwize.
    """
    return 1. if left_val >= right_val else 0.


def score_sqrt_product( left_val: float, right_val: float ) -> float:
    """Get the square product of the left and the right values.

    Args:
        left_val (float): The value of the left entity variable.
        right_val (float): The value of the right entity variable.

    Returns:
        float: The square product of the two values.
    """
    return math.sqrt( left_val * right_val )


def score_log_product( left_val: float, right_val: float ) -> float:
    """Get the log product of the left and the right values.

    Args:
        left_val (float): The value of the left entity variable.
        right_val (float): The value of the right entity variable.

    Returns:
        float: The log of the two values.
    """
    return math.log( 1 + left_val * right_val )


def score_soft_min( left_val: float, right_val: float ) -> float:
    """Get the soft min value between the left and the right values.

    Args:
        left_val (float): The value of the left entity variable.
        right_val (float): The value of the right entity variable.

    Returns:
        float: The soft min value between the two values.
    """
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

    def __init__( self: Self, func: Callable ) -> None:
        """Initialisation of the enum.

        Args:
            func (Callable): The function.
        """
        self.func: Callable = func

    def __str__( self: Self ) -> str:
        """Print the function name.

        Returns:
            str: The name of the function.
        """
        return self.name

    def __call__( self: Self, left_val: float, right_val: float ) -> float:
        """Execute the function of the enum value if it is call.

        Args:
            left_val (float): The value of the left entity variable.
            right_val (float): The value of the right entity variable.

        Returns:
            float: The result of the reward function.
        """
        return self.func( left_val, right_val )
