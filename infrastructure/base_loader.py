# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from abc import ABC, abstractmethod
from typing import Any


class DataLoader( ABC ):
    """Class to load data."""

    @abstractmethod
    def load( self, source: Any ) -> tuple[ tuple[ str, ...], tuple[ dict[ str, str ], ...] ]:
        """Load the data from the source.

        Args:
            source (Any): The data source.

        Returns:
            tuple[tuple[str, ...], tuple[dict[str, str], ...]): The data.
        """
        ...
