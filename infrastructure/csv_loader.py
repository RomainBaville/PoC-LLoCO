# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

import csv
from typing import IO

from infrastructure.base_loader import DataLoader


class CSVLoader( DataLoader ):
    """Class to laod a csv file."""

    def load( self, source: str | IO ):
        """Load CSV from a file path or a file-like object (e.g. Streamlit upload).

        Args:
            source: file path (str) or file-like object

        Returns:
            tuple[tuple[str, ...], tuple[dict[str, str], ...]): The column header of the csv, rows of the csv.
        """
        column: tuple[ str, ...]
        rows: tuple[ dict[ str, str ] ]

        # Case 1: file path
        if isinstance( source, str ):
            with open( source, newline="", encoding="utf-8" ) as f:
                reader = csv.DictReader( f )
                column = tuple( reader.fieldnames ) or ()
                rows = tuple( reader )

        # Case 2: file-like object ( Streamlit )
        else:
            source.seek( 0 )

            content = source.read().decode( "utf-8" ).splitlines()
            reader = csv.DictReader( content )

            column = tuple( reader.fieldnames ) or ()
            rows = tuple( reader )

        return column, rows
