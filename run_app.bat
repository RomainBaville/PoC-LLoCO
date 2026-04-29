@REM SPDX-License-Identifier: Apache-2.0
@REM SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
@REM SPDX-FileContributor: Romain Baville

@echo off
setlocal EnableExtensions EnableDelayedExpansion
title LLoCO Controller

REM =======================
REM CONFIGURATION
REM =======================
set BASE_DIR=%~dp0
set LLAMA_CPP_DIR=%BASE_DIR%llama_cpp
set MODEL_DIR=%BASE_DIR%models
set MODEL_NAME=Qwen2.5-7B-Instruct-Q8_0.gguf
set PORT=8080

set HEALTH_URL=http://localhost:%PORT%/v1/chat/completions

REM =======================
REM START LLAMA SERVER
REM =======================
echo Starting llama-server...
start "llama-server" cmd /k ^
"%LLAMA_CPP_DIR%\llama-server.exe ^
 -m %MODEL_DIR%\%MODEL_NAME% ^
 --port %PORT% ^
 --ctx-size 32768"

REM =======================
REM WAIT FOR SERVER TO BE READY
REM =======================
echo Waiting for llama-server to be ready...

:wait_llama
curl --fail -s -X POST %HEALTH_URL% ^
 -H "Content-Type: application/json" ^
 -d "{\"model\":\"test\",\"messages\":[{\"role\":\"user\",\"content\":\"ping\"}]}" ^
 > nul

if errorlevel 1 (
    timeout /t 3 > nul
    goto wait_llama
)

echo llama-server is ready

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
echo Press E to close llama-server and Streamlit
echo ------------------------------------------

choice /c E /n /m "Press E to exit: "

REM =======================
REM CLEANUP
REM =======================
echo Closing Streamlit...
taskkill /FI "WINDOWTITLE eq streamlit*" /F > nul 2>&1

echo Closing llama-server...
taskkill /FI "WINDOWTITLE eq llama-server*" /F > nul 2>&1

echo Done.
