# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

import csv
from infrastructure.base_loader import DataLoader


class CSVLoader(DataLoader):
    def load(self, path: str):
        try:
            with open(path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                columns = reader.fieldnames or []
                rows = list(reader)
            return columns, rows

        except FileNotFoundError:
            raise RuntimeError(f"CSV file not found: {path}")
