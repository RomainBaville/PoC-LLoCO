# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

import math


# --------------------------------------------------
# Base scoring functions
# --------------------------------------------------

# Reward
def score_min(left, target):
    return min(left, target)


def score_product(left, target):
    return left * target


def score_ratio(left, target):
    if target == 0:
        return 0
    return min(left / target, 1)


def score_threshold(left, target):
    return 1 if left >= target else 0


def score_sqrt_product(left, target):
    return math.sqrt(left * target)


def score_log_product(left, target):
    return math.log(1 + left * target)


def score_soft_min(left, target):
    return (left * target) / (left + target + 1e-6)


# Penalty
def score_shortfall(left, target):
    return -max(0, target - left)


def score_absdiff(left, target):
    return -abs(left - target)


def score_relative_shortfall(left, target):
    if target == 0:
        return 0
    return -max(0, (target - left) / target)


def score_squared_diff(left, target):
    return -(left - target) ** 2


def score_shortfall_squared(left, target):
    return -(max(0, target - left) ** 2)


def score_overqualification(left, target):
    return -max(0, left - target)


def score_log_shortfall(left, target):
    return -math.log(1 + max(0, target - left))

SCORING_FUNCTIONS = {

    # Reward
    "min": score_min,
    "product": score_product,
    "ratio": score_ratio,
    "threshold": score_threshold,
    "sqrt_product": score_sqrt_product,
    "log_product": score_log_product,
    "soft_min": score_soft_min,

    # Penalty
    "shortfall": score_shortfall,
    "absdiff": score_absdiff,
    "relative_shortfall": score_relative_shortfall,
    "squared_diff": score_squared_diff,
    "shortfall_squared": score_shortfall_squared,
    "overqualification": score_overqualification,
    "log_shortfall": score_log_shortfall,
}


class ScoringEngine:
    def __init__(self, config):
        self.config = config

    def compute(self, problem, l, r):
        total = 0

        for s in problem.skills:
            left_val = problem.left_skills[(l, s)]
            target_val = problem.right_requirements[(r, s)]

            # reward
            reward_fn = SCORING_FUNCTIONS[self.config.reward_mode]
            reward = reward_fn(left_val, target_val)

            # penalty (optional)
            penalty = 0
            if self.config.penalty_mode:
                penalty_fn = SCORING_FUNCTIONS[self.config.penalty_mode]
                penalty = penalty_fn(left_val, target_val)

            weight = self.config.skill_weights.get(s, 1)

            total += weight * (reward + self.config.penalty_weight * penalty)

        return int(total)
