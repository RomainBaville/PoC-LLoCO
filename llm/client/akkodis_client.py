# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from pathlib import Path

import requests

ROOT_DIR = Path( __file__ ).resolve().parents[ 2 ]
AKKODIS_OPENAI_API_KEY = "akkodis_openAI_api_key.txt"


def get_akkodis_openai_key() -> str:
    """Get the AKKODIS openAI API key.

    Returns:
        str: The AKKODIS openAI API key.

    Raises:
        ImportError: "No key fund, the "akkodis_openAI_api_key.txt" file must be in the root directory."
    """
    api_key_path: Path = ROOT_DIR / AKKODIS_OPENAI_API_KEY
    if api_key_path.is_file():
        with open( api_key_path, "r", encoding="utf-8" ) as f:
            return f.read().strip()

    raise ImportError( f"No key, the { AKKODIS_OPENAI_API_KEY } file must be in the root folder of the project." )


def ask_akkodis_client( prompt: str, url: str, model_name: str, max_tokens: int = 800, timeout: int = 90 ) -> str:
    """Sends a prompt to the AKKODIS server for the llm wanted.

    Args:
        prompt (str): The prompt to give to the llm.
        url (str): The url of the server with the llm.
        model_name (str): The model to use.
        max_tokens (int): The maximum number of tokens to used.
        timeout (int): The maximum time (s) before crash.

    Returns:
        str: The llm response.

    Raises:
        RuntimeError: AKKODIS API request failed.
        TimeoutError: AKKODIS API request reacht timeout.
    """
    api_key: str = get_akkodis_openai_key()

    headers: dict[ str, str ] = {
        "Content-Type": "application/json",
        "Cache-Control": "no-cache",
        "api-key": api_key,
    }
    payload: dict[ str, int | dict[ str, str ] ] = {
        "max_tokens":
        max_tokens,
        "messages": [
            {
                "role": "system",
                "content":
                ( "You are a professional optimization analyst. "
                  "You explain results clearly and concisely." ),
            },
            {
                "role": "user",
                "content": prompt
            },
        ],
    }

    try:
        resp: requests.Response = requests.post( url, json=payload, headers=headers, timeout=timeout )
        if resp.status_code != 200:
            raise RuntimeError(
                f"AKKODIS API for the model { model_name } request failed { resp.status_code }: { resp.text[ :200 ] }"
            )

        return resp.json()[ "choices" ][ 0 ][ "message" ][ "content" ].strip()
    except requests.exceptions.Timeout as t:
        raise TimeoutError( f"AKKODIS API for the model { model_name } request reacht timeout." ) from t
