# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

import csv

from streamlit.runtime.uploaded_file_manager import UploadedFile
from typing_extensions import Sequence


def load_csv( source: str | UploadedFile ) -> tuple[ tuple[ str, ...], tuple[ dict[ str, str ], ...] ]:
    """Load CSV from a file path or a Streamlit upload file.

    Args:
        source (str | UploadedFile): file path (str) or streamlit upload file (UploadFile).

    Returns:
        tuple[tuple[str, ...], tuple[dict[str, str], ...]]: The column header of the csv, rows of the csv.

    Raises:
        ValueError: The columns of the csv file must have name.
        TypeError: The type of the source is not supported.
    """
    column: tuple[ str, ...]
    rows: tuple[ dict[ str, str ], ...]

    # Case 1: file path
    if isinstance( source, str ):
        with open( source, newline="", encoding="utf-8" ) as file:
            reader = csv.DictReader( file )
            if isinstance( reader.fieldnames, Sequence ):
                column = tuple( reader.fieldnames )
            else:
                raise ValueError( "The columns of the csv file must have name." )

            rows = tuple( reader )

    # Case 2: Streamlit uplaod file
    elif isinstance( source, UploadedFile ):
        source.seek( 0 )

        content = source.read().decode( "utf-8" ).splitlines()
        reader = csv.DictReader( content )

        if isinstance( reader.fieldnames, Sequence ):
            column = tuple( reader.fieldnames )
        else:
            raise ValueError( "The columns of the csv file must have name." )

        rows = tuple( reader )

    else:
        raise TypeError( "The type of the source is not supported." )

    return column, rows
