@REM SPDX-License-Identifier: Apache-2.0
@REM SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
@REM SPDX-FileContributor: Romain Baville

@echo off
setlocal EnableExtensions EnableDelayedExpansion
title LLoCO Controller

@REM REM =======================
@REM REM CONFIGURATION
@REM REM =======================
@REM set BASE_DIR=%~dp0
@REM set LLAMA_CPP_DIR=%BASE_DIR%llama_cpp
@REM set MODEL_DIR=%BASE_DIR%models
@REM set MODEL_NAME=Qwen2.5-7B-Instruct-Q8_0.gguf
@REM set PORT=8080

@REM set HEALTH_URL=http://localhost:%PORT%/v1/chat/completions

@REM REM =======================
@REM REM START LLAMA SERVER
@REM REM =======================
@REM echo Starting llama-server...
@REM start "llama-server" cmd /k ^
@REM "%LLAMA_CPP_DIR%\llama-server.exe ^
@REM  -m %MODEL_DIR%\%MODEL_NAME% ^
@REM  --port %PORT% ^
@REM  --ctx-size 32768"

@REM REM =======================
@REM REM WAIT FOR SERVER TO BE READY
@REM REM =======================
@REM echo Waiting for llama-server to be ready...

@REM :wait_llama
@REM curl --fail -s -X POST %HEALTH_URL% ^
@REM  -H "Content-Type: application/json" ^
@REM  -d "{\"model\":\"test\",\"messages\":[{\"role\":\"user\",\"content\":\"ping\"}]}" ^
@REM  > nul

@REM if errorlevel 1 (
@REM     timeout /t 3 > nul
@REM     goto wait_llama
@REM )

@REM echo llama-server is ready

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

echo Closing llama-server...
taskkill /FI "WINDOWTITLE eq llama-server*" /F > nul 2>&1

echo Done.
