# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

import re
from dataclasses import dataclass
from pathlib import Path

from llm.client.akkodis_client import AKKODIS_MODELS, get_akkodis_openai_key
from llm.client.llama_client import LLAMA_MODELS_DIR

ROOT_DIR = Path( __file__ ).resolve().parents[ 1 ]


@dataclass
class ModelInfo:
    """Dataclass with all the infos of the available LLM.

    Args:
        key (str): Unique identifier.
        label (str):  Label to use for the user.
        model_name (str): Model name sent in the API payload
        source (str): The source of the model.
    """
    key: str
    label: str
    model_name: str
    source: str


def get_llama_models() -> list[ ModelInfo ]:
    """Get all the llama models with the gguf format available.

    Returns:
        list[ModelInfo]: The list with all the models and they infos.
    """
    gguf_files = []
    llama_models_path: Path = ROOT_DIR / LLAMA_MODELS_DIR
    if llama_models_path.is_dir():
        for f in llama_models_path.iterdir():
            if f.suffix != ".gguf":
                continue

            # Keep non-split models
            if "-of-" not in f.name:
                gguf_files.append( f.name )
                continue

            # Keep only the first part of split models
            if re.search( r"-00001-of-\d+\.gguf$", f.name ):
                gguf_files.append( f.name )

    if not gguf_files:
        return []

    return [
        ModelInfo(
            key=f"llama::{ f }",
            model_name=f"{ f }",
            label=f'{ re.sub( r"-00001-of-\d+$", "", f.replace(".gguf", "" ) ) } [llama-server]',
            source="llama-server"
        ) for f in sorted( gguf_files )
    ]


def get_akkodis_models() -> list[ ModelInfo ]:
    """Get all the models available with AKKODIS acces.

    Returns:
        list[ModelInfo]: The list with all the models and they infos.
    """
    try:
        get_akkodis_openai_key()

        return [
            ModelInfo(
                key=f"akkodis::{ model_id }",
                label=label,
                model_name=model_id,
                source="akkodis",
            ) for model_id, label in AKKODIS_MODELS
        ]

    except ImportError:
        return []


def get_models() -> list[ ModelInfo ]:
    """Return all available models across all backends.

    Returns:
        list[ModelInfo]: The list with all the models and they infos.
    """
    return get_akkodis_models() + get_llama_models()
