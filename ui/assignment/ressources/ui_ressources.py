# # SPDX-License-Identifier: Apache-2.0
# # SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# # SPDX-FileContributor: Romain Baville

# import streamlit as st

# from domain.objective import Objective
# from ui.assignment.builder import build_val_dict


# def map_ressources( state ):
#     state.ressources_labels = st.multiselect( "Select columns identifying your ressources", state.left_cols, )
#     state.ressources_vals = build_val_dict( state.left_labels, state.ressources_labels, state.left_rows )


# def ressources_strategy( state ):
#     state.ressoucres_objectives = {}
#     for ressource_label in state.ressources_labels:
#         state.ressoucres_objectives[ ressource_label ] = st.selectbox( f"Select the objective for { ressource_label }", Objective )


# def ressources_constraints( state ):
#     extrema = [ "maximum", "minimum" ]
#     extrema_vals_cols = st.columns( 2 )
#     extrema_vals = [ None, None ]
#     for id, extrema_vals_col in enumerate( extrema_vals_cols ):
#         with extrema_vals_col:
#             use_extrema_vals = st.checkbox( f"Is there ressources with a { extrema[ id ] } constraint per { state.right_labels }" )
#             if use_extrema_vals:
#                 constrainning_variables_labels = st.multiselect( f"Select all variables in the { state.right_entities } used as { extrema[ id ] } constraint", state.right_cols )
#                 constrainning_ressources_labels_map = {}
#                 for constrainning_variable_label in constrainning_variables_labels:
#                     constrainning_ressources_labels_map[ constrainning_variable_label ] = st.multiselect( f"Select ressources constrainning by { constrainning_variable_label }", state.ressources_labels )

#                 vals: dict[ list[ str ], float ] = {}
#                 for right_row in state.right_rows:
#                     right_label: str = right_row[ state.right_entities_col_id ]
#                     for constraint_label, ressources_labels in constrainning_ressources_labels_map.items():
#                         key = [ right_label ]
#                         key.extend( ressources_labels )
#                         vals[ tuple(key) ] = float( right_row[ constraint_label ] )

#                 extrema_vals[ id ] = vals
#             else:
#                 extrema_vals[ id ] = None

#     state.ressoucres_max_vals = extrema_vals[ 0 ]
#     state.ressoucres_min_vals = extrema_vals[ 1 ]
#     print(state.ressoucres_max_vals, "max_vals")
#     print(state.ressoucres_min_vals, "min_vals")


#     extrema_vals_global_cols = st.columns( 2 )
#     extrema_vals_global = [ None, None ]
#     for id, extrema_vals_global_col in enumerate( extrema_vals_global_cols ):
#         with extrema_vals_global_col :
#             use_extrema_vals_global = st.checkbox( f"Is there group of ressources with a { extrema[ id ] } constraint for all { state.right_labels }" )
#             if use_extrema_vals_global:
#                 nb_group = st.number_input( "How many group of ressources are constrained", value=1 )
#                 extrema_vals_global[ id ] = {}
#                 for group in range( nb_group ):
#                     a = st.multiselect( "Select the ressources constrained by the same minimum value for all right entities", state.ressources_labels )
#                     b = st.number_input( f"Set the minimum value constrainning in the same time { a } for all { state.right_label }", value=1 )
#                     extrema_vals_global[ id ][ a ] = b
#             else:
#                 extrema_vals_global[ id ] = None


#     state.ressoucres_max_vals_global = extrema_vals_global[ 0 ]
#     state.ressoucres_min_vals_global = extrema_vals_global[ 1 ]
