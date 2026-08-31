# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from typing import Any

import signal
import requests
import os
import subprocess
import requests
import time
from pathlib import Path
import subprocess
import time
import requests


LLAMA_SERVER_DIR = "llama_cpp"
ROOT_DIR = Path( __file__ ).resolve().parents[ 2 ]

def start_llama_server( url: str, model_name: str ):
    if is_open( url ):
        raise ValueError( "A llama server is already open." )

    if os.path.isdir( LLAMA_SERVER_DIR ):
        llama_exe_path =  str( ROOT_DIR / "llama_cpp/llama-server.exe" )
    else:
        raise ImportError( "The folder llama_cpp is not in the root directory." )

    model_path = str( ROOT_DIR / f"models/{ model_name }.gguf" )

    llama_server = subprocess.Popen(
        [
            llama_exe_path,
            "-m", model_path,
            "--port", url[ -4: ],
            "--ctx-size", "32768"
        ],
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
    )
    llama_server_open: bool = False
    retry: int = 0
    while not llama_server_open and retry < 10:
        llama_server_open = is_open( url )
        time.sleep( 30 )
        retry += 1

    if not llama_server_open:
        raise TimeoutError( "The llama sevrer was to long to open." )
    else:
        print( "The llama server is open." )
        return llama_server


def close_llama_server( llama_server ):
    llama_server.send_signal(signal.CTRL_BREAK_EVENT)
    print( "The llama server is close.")


def is_open( url ):
    try:
        response = requests.post(
            f"{ url }/v1/chat/completions",
            json={
                "model": "test",
                "messages": [ { "role": "user", "content": "ping" } ]
            },
            timeout=5
        )

        if response.status_code == 200:
            return True

    except requests.exceptions.RequestException:
        return False


def ask_llama_client( prompt: str, url: str, model_name: str, max_tokens: int = 800, max_retries: int = 3 ) -> str:
    """Send a prompt to the local LLM and return the response text.

    Args:
        prompt (str): The prompt to give to the llm.

    Returns:
        str: The llm response.
    """
    payload: dict[ str, Any ] = {
        "model": model_name,
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
        "temperature": 0.2,
        "top_p": 0.9,
        "max_tokens": max_tokens,
        "stream": False
    }

    response = requests.post(
        url=f"{ url }/v1/chat/completions",
        json=payload,
        timeout=3600
    )

    if response.status_code != 200:
        raise RuntimeError( f"LLM request failed "
                            f"({response.status_code}): {response.text}" )

    data = response.json()

    try:
        content: str = str( data[ "choices" ][ 0 ][ "message" ][ "content" ].strip() )
        return content
    except ( KeyError, IndexError ) as e:
        raise RuntimeError( f"Unexpected LLM response format: {data}" ) from e
