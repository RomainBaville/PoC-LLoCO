# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

def apply_cost_constraints( model, x, problem ):
    if problem.use_costs:
        if problem.costs_config.limit_costs_label is not None:
            for right in problem.right_entities:
                for cost, limit in problem.costs_config.limit_costs_label.items():
                    limit_cost = problem.costs_config.limit_costs_val[ right, limit ]
                    model.Add( sum( problem.costs_config.costs_val[ left, cost ] * x[ left, right ] for left in problem.left_entities ) <= int( limit_cost ) )
