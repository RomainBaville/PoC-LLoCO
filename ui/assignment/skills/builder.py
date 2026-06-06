# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

def build_skills_val( entities: list[ str ], skills_label: list[ str ], rows ):
    skills_val: dict[ list[ str ], float ] = {}
    for i, row in enumerate( rows ):
        entity: str = entities[ i ]
        for skill in skills_label:
            skills_val[ ( entity, skill ) ] = float( row[ skill ] )

    return skills_val