# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

def apply_cost_constraints( model, x, problem ):
    if problem.use_costs:
        costs_config = problem.costs_config
        if costs_config.limit_costs_entities_val is not None:
            for ( right, limit_cost_entities_label ), limit_cost_entities_val in costs_config.limit_costs_val.items():
                cost_entities_limited_label = costs_config.limit_costs_entities_label[ limit_cost_entities_label ]
                model.Add( sum( costs_config.costs_val[ left, cost_entities_limited_label ] * x[ left, right ] for left in problem.left_entities ) <= int( limit_cost_entities_val ) )


        if costs_config.limit_all_costs_entities_val is not None:
            for right, limit_all_costs_entity_val in costs_config.limit_all_costs_entities_val.items():
                model.Add( sum( costs_config.costs_val[ left, cost_label ] * x[ left, right ] for cost_label in costs_config.costs_label for left in problem.left_entities ) <= int( limit_all_costs_entity_val ) )


        if costs_config.limit_costs_all_entities_val is not None:
            for cost_all_entities_limited_label, limit_cost_all_entities_val in costs_config.limit_costs_all_entities_val.items():
                model.Add( sum( costs_config.costs_val[ left, cost_all_entities_limited_label ] * x[ left, right ] for left, right in x ) <= int( limit_cost_all_entities_val ) )


        if costs_config.limit_all_costs_all_entities_val is not None:
            model.Add( sum( costs_config.costs_val[ left, cost ] * x[ left, right ] for cost in costs_config.costs_label for left, right in x ) <= int( costs_config.limit_all_costs_all_entities_val ) )
