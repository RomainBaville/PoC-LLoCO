# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville
# ruff: noqa: E402 # disable Module level import not at top of file

import sys
from pathlib import Path

# --- make project root importable ---
ROOT_DIR = Path( __file__ ).resolve().parents[ 1 ]
sys.path.append( str( ROOT_DIR ) )

from launcher.utils import start_process, stop_process

STREAMLIT_APP: Path = Path( "ui/app.py" )


def main() -> None:
    """Launch the streamlit app."""
    print( "Starting Streamlit..." )

    command: list[ str ] = [ "streamlit", "run", str( STREAMLIT_APP ) ]
    process_id: int = start_process( command, "Streamlit App" )

    print( "------------------------------------------" )
    print( "Press Q to close Streamlit" )
    print( "------------------------------------------" )

    try:
        while input( "Press Q to quit: " ).strip().upper() != "Q":
            pass
    finally:
        print( "Closing Streamlit..." )

        stop_process( process_id )

        print( "Done." )


if __name__ == "__main__":
    main()
