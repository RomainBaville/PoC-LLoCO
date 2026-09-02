# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville
"""Client for the AKKODIS Azure OpenAI endpoint.
Mirrors the logic from LLoCO/llm_utils.py — same URL pattern, same auth header.
"""

import os
import time
from typing import Optional

import requests

_API_KEY_SEARCH_PATHS = [ os.path.join( os.getcwd(), ".api_key.txt" ), os.path.join( os.getcwd(), "api_key.txt" ) ]


def find_api_key() -> Optional[ str ]:
    key = os.environ.get( "OPENAI_API_KEY" )
    if key:
        return key
    for path in _API_KEY_SEARCH_PATHS:
        if os.path.isfile( path ):
            with open( path, "r", encoding="utf-8" ) as f:
                return f.read().strip()
    return None


def ask_akkodis_client(
    prompt: str, url: str, model_name: str = "", max_tokens: int = 800, max_retries: int = 3
) -> str:
    api_key = find_api_key()
    if not api_key:
        raise RuntimeError(
            "Clé API AKKODIS introuvable. "
            "Placez un fichier .api_key.txt à la racine du projet "
            "ou définissez OPENAI_API_KEY."
        )

    headers = {
        "Content-Type": "application/json",
        "Cache-Control": "no-cache",
        "api-key": api_key,
    }
    payload = {
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

    for attempt in range( max_retries ):
        try:
            resp = requests.post( url, json=payload, headers=headers, timeout=90 )
            if resp.status_code == 429 or resp.status_code >= 500:
                time.sleep( 2**attempt )
                continue
            if resp.status_code != 200:
                raise RuntimeError( f"AKKODIS API error {resp.status_code}: {resp.text[:200]}" )
            return resp.json()[ "choices" ][ 0 ][ "message" ][ "content" ].strip()
        except requests.exceptions.Timeout:
            if attempt == max_retries - 1:
                raise RuntimeError( "AKKODIS API timeout." )
            time.sleep( 2**attempt )

    raise RuntimeError( "AKKODIS API : nombre maximum de tentatives atteint." )
