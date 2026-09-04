# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

import time
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import requests

from launcher.utils import start_process, stop_process

ROOT_DIR: Path = Path( __file__ ).resolve().parents[ 2 ]

LLAMA_MODELS_DIR: str = "models"
LLAMA_SERVER_DIR: str = "llama_cpp"
LLAMA_SERVER_EXE: str = "llama-server.exe"
LLAMA_SERVER_URL: str = "http://localhost:8080"


def start_llama_server( model_name: str, timeout: int = 300, llama_server_pid: int = 0 ) -> int:
    """Open a llama server with the wanted model if it is not.

    Args:
        model_name (str): The model to use.
        timeout (int): The maximum time (s) before crash.
            defaults to 300.
        llama_server_pid (int): The pid of the Popen subprocess with the llama server open.
            Defaults to 0 (no subprocess pid).

    Returns:
        int: The pid of the Popen subprocess with the llama serve open.

    Raises:
        ImportError: Something went wrong with the url or the model_name.
        TimeoutError: The llama sevrer was to long to open.
    """
    llama_exe_path: Path = ROOT_DIR / LLAMA_SERVER_DIR / LLAMA_SERVER_EXE
    if not llama_exe_path.is_file():
        raise ImportError( f"No { LLAMA_SERVER_EXE }, the folder { LLAMA_SERVER_DIR } must be in the root directory." )

    model_path: Path = ROOT_DIR / LLAMA_MODELS_DIR / model_name
    if not model_path.is_file():
        raise ImportError( f"The model { model_name } is not in the folder { LLAMA_MODELS_DIR } of the project." )

    if llama_server_pid != 0:
        if is_open( model_path ):
            return llama_server_pid
        else:
            stop_process( llama_server_pid )

    port: int | None = urlparse( LLAMA_SERVER_URL ).port
    if port is None:
        raise ImportError( "fail to get the port in the llama server url." )

    command: list[ str ] = [
        str( llama_exe_path ), "-m", str( model_path ), "--port", str( port ), "--ctx-size", "32768"
    ]
    llama_server_pid = start_process( command, "LLama server" )

    llama_server_open: bool = False
    retry: int = 0
    while not llama_server_open and retry < timeout:
        llama_server_open = is_open()
        time.sleep( int( timeout / 60 ) )
        retry += int( timeout / 60 )

    if not llama_server_open:
        raise TimeoutError( "The llama sevrer was to long to open." )

    print( "The llama server is open." )
    return llama_server_pid


def is_open( expected_model: Path | None = None ) -> bool:
    """Check if a llama server is open ant its model if needed.

    Args:
        expected_model (Path | None): The path to the model expected to be used.
            Defaults to None (the model is not check).

    Returns:
        bool: True if the server is open, False otherwise.
    """
    try:
        response = requests.get( f"{ LLAMA_SERVER_URL }/v1/models", timeout=5 )

        if response.status_code != 200:
            return False

        if expected_model is None:
            return True

        models = response.json().get( "data", [] )

        for model in models:
            model_id = model.get( "id", "" )

            # Exact match
            if str( model_id ) == str( expected_model ):
                return True

        return False

    except requests.exceptions.RequestException:
        return False


def ask_llama_client( prompt: str, model_name: str, max_tokens: int = 800, timeout: int = 3600 ) -> str:
    """Sends a prompt to the llama-server for the llm wanted.

    Args:
        prompt (str): The prompt to give to the llm.
        model_name (str): The model to use.
        max_tokens (int): The maximum number of tokens to used.
        timeout (int): The maximum time (s) before crash.

    Returns:
        str: The llm response.

    Raises:
        RuntimeError: LLama-server request failed.
        TimeoutError: LLama-server request reacht timeout.
    """
    payload: dict[ str, Any ] = {
        "model":
        model_name,
        "messages": [
            {
                "role": "system",
                "content":
                ( "You are a professional optimization analyst. "
                  "You explain results clearly and concisely." ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        "temperature":
        0.2,
        "top_p":
        0.9,
        "max_tokens":
        max_tokens,
        "stream":
        False
    }
    url: str = f"{ LLAMA_SERVER_URL }/v1/chat/completions"

    try:
        resp: requests.Response = requests.post( url=url, json=payload, timeout=timeout )
        if resp.status_code != 200:
            raise RuntimeError(
                f"LLama-server for the model { model_name } request failed { resp.status_code }: { resp.text[ :200 ] }"
            )

        return str( resp.json()[ "choices" ][ 0 ][ "message" ][ "content" ].strip() )
    except requests.exceptions.Timeout as t:
        raise RuntimeError( f"LLama-server for the model { model_name } request reacht timeout." ) from t
