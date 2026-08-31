@REM SPDX-License-Identifier: Apache-2.0
@REM SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
@REM SPDX-FileContributor: Romain Baville

@echo off
setlocal EnableExtensions EnableDelayedExpansion
title LLoCO Controller

REM =======================
REM START STREAMLIT
REM =======================
echo Starting Streamlit...
start "streamlit" cmd /k ^
"streamlit run ui\app.py"

REM =======================
REM WAIT FOR USER EXIT
REM =======================
echo ------------------------------------------
echo Press Q to close llama-server and Streamlit
echo ------------------------------------------

choice /c Q /n /m "Press Q to quit: "

REM =======================
REM CLEANUP
REM =======================
echo Closing Streamlit...
taskkill /FI "WINDOWTITLE eq streamlit*" /F > nul 2>&1

echo Done.
