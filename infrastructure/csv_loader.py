# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

import csv
from infrastructure.base_loader import DataLoader

import csv
from typing import IO

class CSVLoader(DataLoader):

    def load(self, source: str | IO ):
        """
        Load CSV from a file path or a file-like object (e.g. Streamlit upload).

        Args:
            source: file path (str) or file-like object

        Returns:
            columns (list[str])
            rows (list[dict])
        """
        try:
            # Case 1: file path
            if isinstance( source, str ):
                with open( source, newline = "", encoding = "utf-8" ) as f:
                    reader = csv.DictReader( f )
                    columns = reader.fieldnames or []
                    rows = list( reader )

            # Case 2: file-like object (Streamlit)
            else:
                # Important: ensure we're at start of file
                source.seek( 0 )

                content = source.read().decode( "utf-8" ).splitlines()
                reader = csv.DictReader( content )

                columns = reader.fieldnames or []
                rows = list( reader )

            return columns, rows

        except FileNotFoundError:
            raise RuntimeError( f"CSV file not found: { source }" )
