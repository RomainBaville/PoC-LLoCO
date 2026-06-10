# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

def apply_cost_constraints( model, x, problem ):
    if problem.use_costs:
        costs_config = problem.costs_config
        if costs_config.limit_costs_val is not None:
            costs_label = costs_label.keys()
            for ( right, limit_cost_label ), limit_val in costs_config.limit_costs_val.items():
                i = 0
                while limit_cost_label not in costs_config.costs_label[ costs_label[ i ] ]:
                    i += 1
                cost_label = costs_label[ i ]
                model.Add( sum( costs_config.costs_val[ left, cost_label ] * x[ left, right ] for left in problem.left_entities ) <= int( limit_val ) )

        if costs_config.limit_entities_costs_val is not None:
            for right, limit_val in costs_config.limit_entities_costs_val.items():
                model.Add( sum( costs_config.costs_val[ left, cost_label ] * x[ left, right ] for cost_label in costs_config.costs_label for left in problem.left_entities ) )

        if costs_config.limit_assignment_costs_val is not None:
            model.Add( sum( costs_config.costs_val[ left, cost ] * x[ left, right ] for cost in costs_config.costs_label for left, right in x ) )
