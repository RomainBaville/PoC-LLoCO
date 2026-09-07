# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

import io
import zipfile


def build_results_zip( summary: str ) -> bytes:
    """Build a ZIP file containing: ai_summary.txt.

    Args:
        summary (str): The summary of the problem.

    Returns:
        bytes: A zip folder with the summary of the problem.
    """
    buffer = io.BytesIO()

    with zipfile.ZipFile( buffer, mode="w", compression=zipfile.ZIP_DEFLATED ) as zf:
        # -----------------------------
        # AI Summary
        # -----------------------------
        zf.writestr( "ai_summary.txt", summary )

    buffer.seek( 0 )
    return buffer.read()
