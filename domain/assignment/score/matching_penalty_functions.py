# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

import math
from collections.abc import Callable
from enum import Enum
from typing import Self


def no_penalty( left_val: float, right_val: float ) -> float:
    """No penalty.

    Args:
        left_val (float): The value of the left entity variable.
        right_val (float): The value of the right entity variable.

    Returns:
        float: 0.
    """
    return 0.


def score_shortfall( left_val: float, right_val: float ) -> float:
    """Get the max value between 0. and the difference of the left and the right values.

    Args:
        left_val (float): The value of the left entity variable.
        right_val (float): The value of the right entity variable.

    Returns:
        float: The result.
    """
    return -max( 0., right_val - left_val )


def score_absdiff( left_val: float, right_val: float ) -> float:
    """Get absolute difference of the left and the right values.

    Args:
        left_val (float): The value of the left entity variable.
        right_val (float): The value of the right entity variable.

    Returns:
        float: The result.
    """
    return -abs( left_val - right_val )


def score_relative_shortfall( left_val: float, right_val: float ) -> float:
    """Get the relative shortfall value between the left and the right values.

    Args:
        left_val (float): The value of the left entity variable.
        right_val (float): The value of the right entity variable.

    Returns:
        float: The result.
    """
    if right_val == 0:
        return 0.
    return -max( 0., ( right_val - left_val ) / right_val )


def score_squared_diff( left_val: float, right_val: float ) -> float:
    """Get the square difference of the left and the right values.

    Args:
        left_val (float): The value of the left entity variable.
        right_val (float): The value of the right entity variable.

    Returns:
        float: The result.
    """
    return -( left_val - right_val )**2


def score_shortfall_squared( left_val: float, right_val: float ) -> float:
    """Get the square shortfall value between the left and the right values.

    Args:
        left_val (float): The value of the left entity variable.
        right_val (float): The value of the right entity variable.

    Returns:
        float: The result.
    """
    return -( max( 0., right_val - left_val )**2 )


def score_overqualification( left_val: float, right_val: float ) -> float:
    """0. if the left val is higher than the right val.

    Args:
        left_val (float): The value of the left entity variable.
        right_val (float): The value of the right entity variable.

    Returns:
        float: The result.
    """
    return -max( 0., left_val - right_val )


def score_log_shortfall( left_val: float, right_val: float ) -> float:
    """Get the log shortfall value between the left and the right values.

    Args:
        left_val (float): The value of the left entity variable.
        right_val (float): The value of the right entity variable.

    Returns:
        float: The result.
    """
    return -math.log( 1. + max( 0., right_val - left_val ) )


class PenaltyFunctions( Enum ):
    """Enum for penalty functions."""
    NONE = ( no_penalty, )
    SHORTFALL = ( score_shortfall, )
    ABS_DIFF = ( score_absdiff, )
    RELATIVE_SHORTFALL = ( score_relative_shortfall, )
    SQUARED_DIFF = ( score_squared_diff, )
    SHORTFALL_SQUARED = ( score_shortfall_squared, )
    OVERQUALIFICATION = ( score_overqualification, )
    LOG_SHORTFALL = ( score_log_shortfall, )

    def __init__( self: Self, func: Callable[ [ float, float ], float ] ):
        """Initialisation of the enum.

        Args:
            func (Callable[[float, float], float]): The function.
        """
        self.func: Callable[ [ float, float ], float ] = func

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
            float: The result of the penalty function.
        """
        return self.func( left_val, right_val )
