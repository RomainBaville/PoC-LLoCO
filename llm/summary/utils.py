# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

import io
import zipfile


def build_results_zip(
    solution_rows: list[ dict[ str, str ] ],
    ai_summary: str,
) -> bytes:
    """Build a ZIP file containing: solution.csv, ai_summary.txt and metadata.json.

    Args:
        solution_rows (list[dict[str, str]]): The solution of the problem.
        ai_summary (str): The summary of the problem.

    Returns:
        bytes: A zip folder with the summary and the solution of the problem.
    """
    buffer = io.BytesIO()

    with zipfile.ZipFile( buffer, mode="w", compression=zipfile.ZIP_DEFLATED ) as zf:

        # -----------------------------
        # Solution CSV
        # -----------------------------
        headers = solution_rows[ 0 ].keys()
        csv_content = ",".join( headers ) + "\n"
        csv_content += "\n".join( ",".join( str( row[ h ] ) for h in headers ) for row in solution_rows )
        zf.writestr( "solution.csv", csv_content )

        # -----------------------------
        # AI Summary
        # -----------------------------
        zf.writestr( "ai_summary.txt", ai_summary )

    buffer.seek( 0 )
    return buffer.read()
