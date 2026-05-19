# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from typing import Dict, List, Tuple


class EntityRegistry:
    """
    Global registry to manage entity identities.

    - Generates guaranteed-unique internal IDs
    - Stores human-readable labels
    - Keeps solver models safe from name collisions
    """

    def __init__(self, prefix: str):
        self.prefix = prefix
        self._counter = 0
        self.labels: Dict[str, str] = {}

    def create(self, label: str) -> str:
        internal_id = f"{self.prefix}_{self._counter}"
        self._counter += 1
        self.labels[internal_id] = label
        return internal_id


def check_unique_identifiers(
    rows: List[dict],
    id_cols: List[str],
) -> List[str]:
    """
    Check that selected identifier columns uniquely identify rows.

    Returns a list of duplicated identifiers (display form).
    """
    seen: set[Tuple[str, ...]] = set()
    duplicates: set[str] = set()

    for row in rows:
        key = tuple(row[c] for c in id_cols)
        if key in seen:
            duplicates.add(" ".join(key))
        seen.add(key)

    return sorted(duplicates)
