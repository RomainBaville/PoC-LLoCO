# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville
"""Detects locally available LLM models and returns connection metadata.
Currently supports:
  - Ollama  (http://localhost:11434)
  - llama-server GGUF  (models/ directory)
"""

import os
import re
from dataclasses import dataclass

import requests

from llm.client.akkodis_client import get_akkodis_openai_key

AKKODIS_URL = "https://cld.akkodis.com/api/openai/deployments/models-{model}/chat/completions?api-version=2024-12-01-preview"
LLAMA_SERVER_URL = "http://localhost:8080"
_OLLAMA_URL = "http://localhost:11434"

AKKODIS_MODELS = [
    ( "gpt-4o-mini", "GPT-4o mini  [AKKODIS]" ), ( "gpt-4o", "GPT-4o  [AKKODIS]" ), ( "gpt-5", "GPT-5  [AKKODIS]" ),
    ( "o4-mini", "o4-mini  [AKKODIS]" )
]
LLAMA_MODELS_DIR = "models"

_TIMEOUT = 1.5


@dataclass
class ModelInfo:
    key: str  # unique identifier used in session state
    label: str  # displayed in the selectbox
    api_url: str  # OpenAI-compatible completions endpoint
    model_name: str  # model name sent in the API payload
    source: str  # "ollama" | "llama-server" | "akkodis"


def _discover_ollama() -> list[ ModelInfo ]:
    try:
        resp = requests.get( f"{_OLLAMA_URL}/api/tags", timeout=_TIMEOUT )
        if resp.status_code != 200:
            return []
        models = resp.json().get( "models", [] )
        result = []
        for m in models:
            name = m.get( "name", "" )
            if not name:
                continue
            result.append(
                ModelInfo(
                    key=f"ollama::{name}",
                    label=f"{name}  [Ollama]",
                    api_url=f"{_OLLAMA_URL}/v1/chat/completions",
                    model_name=name,
                    source="ollama",
                )
            )
        return result
    except Exception:
        return []


def get_llama_models() -> list[ ModelInfo ]:
    gguf_files = []
    if os.path.isdir( LLAMA_MODELS_DIR ):
        for f in os.listdir( LLAMA_MODELS_DIR ):
            if not f.endswith( ".gguf" ):
                continue

            # Keep non-split models
            if "-of-" not in f:
                gguf_files.append( f )
                continue

            # Keep only the first part of split models
            if re.search( r"-00001-of-\d+\.gguf$", f ):
                gguf_files.append( f )

    if not gguf_files:
        return []

    return [
        ModelInfo(
            key=f"llama::{ f }",
            model_name=f"{ f }",
            api_url=LLAMA_SERVER_URL,
            label=f'{ re.sub( r"-00001-of-\d+$", "", f.replace(".gguf", "" ) ) } [llama-server]',
            source="llama-server"
        ) for f in sorted( gguf_files )
    ]


def get_akkodis_models() -> list[ ModelInfo ]:
    try:
        get_akkodis_openai_key()

        return [
            ModelInfo(
                key=f"akkodis::{model_id}",
                label=label,
                api_url=AKKODIS_URL.format( model=model_id ),
                model_name=model_id,
                source="akkodis",
            ) for model_id, label in AKKODIS_MODELS
        ]

    except ImportError:
        return []


def get_models() -> list[ ModelInfo ]:
    """Return all available models across all backends."""
    return get_akkodis_models() + _discover_ollama() + get_llama_models()
