# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from dataclasses import dataclass
from typing import Callable, Type

from domain.assignment.skills.coverage import SkillCoverageAssignment
from domain.assignment.skills.best_fit import SkillBestFitAssignment
from domain.assignment.skills.team import SkillTeamAssignment
from domain.assignment.skills.portfolio import SkillPortfolioSelection


@dataclass
class AssignmentVariant:
    key: str
    label: str
    description: str
    render_fn: str
    domain_class: Type
    builder_fn: Callable


# --------------------------------------------------
# Builder functions (kept close to variant metadata)
# --------------------------------------------------

def build_skills_coverage(data):
    return SkillCoverageAssignment(
        **data,
        max_assignments_per_left=1,
    )


def build_skills_best_fit(data):
    return SkillBestFitAssignment(
        left_entities=data["left_entities"],
        right_entities=data["right_entities"],
        skills=data["skills"],
        left_skills=data["left_skills"],
        target_preferences=data["right_requirements"],
        max_assignments_per_left=1,
    )


def build_skills_team(data):
    return SkillTeamAssignment(
        **data,
        team_requirements=data["right_requirements"],
        min_team_size={r: 1 for r in data["right_entities"]},
        max_team_size={r: len(data["left_entities"]) for r in data["right_entities"]},
    )


def build_skills_portfolio(data):
    skill_requirements = {
        s: max(
            data["right_requirements"].get((r, s), 0)
            for r in data["right_entities"]
        )
        for s in data["skills"]
    }

    return SkillPortfolioSelection(
        left_entities=data["left_entities"],
        skills=data["skills"],
        left_skills=data["left_skills"],
        skill_requirements=skill_requirements,
    )


# --------------------------------------------------
# Variant registry
# --------------------------------------------------

VARIANTS = {
    "coverage": AssignmentVariant(
        key="coverage",
        label="Skill coverage",
        description="Assign entities so that all required skills are fully covered",
        render_fn="ui.problems.assignment.skills.ui_coverage.render",
        domain_class=SkillCoverageAssignment,
        builder_fn=build_skills_coverage,
    ),
    "best_fit": AssignmentVariant(
        key="best_fit",
        label="Best-fit matching",
        description="Match entities to maximize skill compatibility",
        render_fn="ui.problems.assignment.skills.ui_best_fit.render",
        domain_class=SkillBestFitAssignment,
        builder_fn=build_skills_best_fit,
    ),
    "team": AssignmentVariant(
        key="team",
        label="Team formation",
        description="Form multi-person teams that jointly cover skills",
        render_fn="ui.problems.assignment.skills.ui_team.render",
        domain_class=SkillTeamAssignment,
        builder_fn=build_skills_team,
    ),
    "portfolio": AssignmentVariant(
        key="portfolio",
        label="Skill portfolio selection",
        description="Select a subset of entities whose skills cover requirements",
        render_fn="ui.problems.assignment.skills.ui_portfolio.render",
        domain_class=SkillPortfolioSelection,
        builder_fn=build_skills_portfolio,
    ),
}
