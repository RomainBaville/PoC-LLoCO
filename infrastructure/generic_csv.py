# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

import csv

def load_csv(path: str):
    """
    Generic CSV loader.
    Returns:
      - columns: list[str]
      - rows: list[dict[column -> value]]
    """
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        columns = reader.fieldnames

    return columns, rows