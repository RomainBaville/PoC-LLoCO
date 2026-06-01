# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

def apply_logical_constraints(model, x, problem):
    cfg = problem.config

    if getattr(cfg, "mutual_exclusion", None):
        for (l1, r1), (l2, r2) in cfg.mutual_exclusion:
            model.Add(x[l1, r1] + x[l2, r2] <= 1)

    if getattr(cfg, "implications", None):
        for (l1, r1), (l2, r2) in cfg.implications:
            model.Add(x[l1, r1] <= x[l2, r2])

    if getattr(cfg, "group_limits", None):
        for group, max_val in cfg.group_limits:
            model.Add(
                sum(x[l, r] for (l, r) in group) <= max_val
            )
