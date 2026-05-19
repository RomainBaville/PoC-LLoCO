# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from dataclasses import dataclass
from typing import Callable, Dict

from infrastructure.csv_loader import CSVLoader


@dataclass
class DataSourceDefinition:
    key: str
    label: str
    description: str
    loader_factory: Callable


DATA_SOURCE_REGISTRY: Dict[str, DataSourceDefinition] = {

    "csv_two_tables": DataSourceDefinition(
        key="csv_two_tables",
        label="Two CSV files (entities + requirements)",
        description=(
            "You have two CSV files: one describing entities "
            "(e.g. employees) and one describing requirements "
            "(e.g. projects)."
        ),
        loader_factory=lambda: CSVLoader(),
    ),

    # Future examples:
    # "csv_single_table"
    # "matrix_input"
    # "manual_input"
}
