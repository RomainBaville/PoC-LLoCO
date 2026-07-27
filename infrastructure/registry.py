# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from collections.abc import Callable
from dataclasses import dataclass

from infrastructure.base_loader import DataLoader
from infrastructure.csv_loader import CSVLoader


@dataclass
class DataSourceDefinition:
    """Dataclass to deal with several type of input data.

    Args:
        key (str): The key of the input data use for the code.
        label (str): The label of the input data use for the user.
        description (str): The description of the input data.
        loader_class (Callable[[], DataLoader]): The class used to load the data.
    """
    key: str
    label: str
    description: str
    loader_class: Callable[ [], DataLoader ]


DATA_SOURCE_REGISTRY: dict[ str, DataSourceDefinition ] = {
    "csv_two_tables":
    DataSourceDefinition(
        key="csv_two_tables",
        label="Two CSV files",
        description=( "You have two CSV files, one with the data and the other with the constraints." ),
        loader_class=CSVLoader,
    ),
}
