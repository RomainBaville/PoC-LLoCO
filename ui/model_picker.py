# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.

"""
Detects locally available LLM models and returns connection metadata.
Currently supports:
  - Ollama  (http://localhost:11434)
  - llama-server GGUF  (models/ directory)
"""

import os
from dataclasses import dataclass
from typing import Optional

import requests

_OLLAMA_URL = "http://localhost:11434"
_LLAMA_SERVER_URL = "http://localhost:8080"
_MODELS_DIR = "models"
_TIMEOUT = 1.5


@dataclass
class ModelInfo:
    key: str          # unique identifier used in session state
    label: str        # displayed in the selectbox
    api_url: str      # OpenAI-compatible completions endpoint
    model_name: str   # model name sent in the API payload
    source: str       # "ollama" | "llama-server" | "akkodis"


def _discover_ollama() -> list[ModelInfo]:
    try:
        resp = requests.get(f"{_OLLAMA_URL}/api/tags", timeout=_TIMEOUT)
        if resp.status_code != 200:
            return []
        models = resp.json().get("models", [])
        result = []
        for m in models:
            name = m.get("name", "")
            if not name:
                continue
            result.append(ModelInfo(
                key=f"ollama::{name}",
                label=f"{name}  [Ollama]",
                api_url=f"{_OLLAMA_URL}/v1/chat/completions",
                model_name=name,
                source="ollama",
            ))
        return result
    except Exception:
        return []


def _discover_llama_server() -> list[ModelInfo]:
    gguf_files = []
    if os.path.isdir(_MODELS_DIR):
        gguf_files = [f for f in os.listdir(_MODELS_DIR) if f.endswith(".gguf")]

    if not gguf_files:
        return []

    # Check if llama-server is reachable
    try:
        requests.get(f"{_LLAMA_SERVER_URL}/health", timeout=_TIMEOUT)
    except Exception:
        return []

    return [
        ModelInfo(
            key=f"llama::{f}",
            label=f"{f}  [llama-server]",
            api_url=f"{_LLAMA_SERVER_URL}/v1/chat/completions",
            model_name=f.replace(".gguf", ""),
            source="llama-server",
        )
        for f in gguf_files
    ]


def _discover_akkodis() -> list[ModelInfo]:
    from ui.akkodis_client import find_api_key, AKKODIS_MODELS, _BASE_URL
    if not find_api_key():
        return []
    return [
        ModelInfo(
            key=f"akkodis::{model_id}",
            label=label,
            api_url=_BASE_URL.format(model=model_id),
            model_name=model_id,
            source="akkodis",
        )
        for model_id, label in AKKODIS_MODELS
    ]


def discover() -> list[ModelInfo]:
    """Return all available models across all backends."""
    return _discover_akkodis() + _discover_ollama() + _discover_llama_server()


def get_by_key(key: str) -> Optional[ModelInfo]:
    for m in discover():
        if m.key == key:
            return m
    return None
