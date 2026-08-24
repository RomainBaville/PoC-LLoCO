# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from streamlit.runtime.state.session_state_proxy import SessionStateProxy

from domain.assignment.score.matching_config import MatchingConfig
from domain.assignment.score.ressources_config import RessourcesConfig
from domain.assignment.score.score_config import ScoreConfig


def build_score_config( state: SessionStateProxy ) -> ScoreConfig:
    """Build the score config of the assignment problem.

    Args:
        state (SessionStateProxy): The session state.

    Returns:
        ScoreConfig: The configuration of the score of the assignment problem
    """
    matching_config: MatchingConfig | None = None
    if state.use_matching:
        matching_config = MatchingConfig(
            labels=state.matching_labels,
            left_vals=state.matching_left_vals,
            right_vals=state.matching_right_vals,
            objective=state.matching_objective,
            weights=state.matching_weights,
            reward_function=state.reward_function,
            penalty_function=state.penalty_function,
            max_vals=state.matching_max_vals,
            min_vals=state.matching_min_vals,
        )

    ressources_config: RessourcesConfig | None = None
    if state.use_ressources:
        ressources_config = RessourcesConfig(
            labels=state.ressources_labels,
            vals=state.ressources_vals,
            objectives=state.ressoucres_objectives,
            weights=state.ressources_weights,
            max_vals=state.constraints_max_vals,
            min_vals=state.constraints_min_vals,
            max_global_vals=state.constraints_max_global_vals,
            min_global_vals=state.constraints_min_global_vals,
        )

    score_config: ScoreConfig = ScoreConfig(
        use_matching=state.use_matching,
        matching_config=matching_config,
        use_ressources=state.use_ressources,
        ressources_config=ressources_config,
    )

    return score_config
