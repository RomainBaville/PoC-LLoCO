# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

import subprocess
from pathlib import Path

STREAMLIT_APP = Path( "ui/app.py" )

print( "Starting Streamlit..." )

process = subprocess.Popen(
    [ "streamlit", "run", STREAMLIT_APP ],
    creationflags=subprocess.CREATE_NEW_CONSOLE,
)

print( "------------------------------------------" )
print( "Press Q to close Streamlit" )
print( "------------------------------------------" )

while input( "Press Q to quit: " ).strip().upper() != "Q":
    pass

print( "Closing Streamlit..." )

subprocess.run(
    [ "taskkill", "/PID", str( process.pid ), "/T", "/F" ],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)

print( "Done." )
