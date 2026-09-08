# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville, Fidel Monteiro

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Self

from llm.client.akkodis_client import AKKODIS_MODELS, get_akkodis_openai_api_key
from llm.client.llama_client import LLAMA_MODELS_DIR, LLAMA_SERVER_DIR, LLAMA_SERVER_EXE

ROOT_DIR = Path( __file__ ).resolve().parents[ 1 ]


@dataclass
class ModelInfo:
    """Dataclass with all the infos of the available LLM.

    Args:
        label (str):  Label to use for the user.
        model_name (str): Model name sent in the API payload
        source (str): The source of the model.
    """
    label: str
    name: str
    source: str

    def __str__( self: Self ) -> str:
        """Print the label of the model.

        Returns:
            str: The label of the model.
        """
        return self.label


def get_llama_models() -> list[ ModelInfo ]:
    """Get all the llama models with the gguf format available.

    Returns:
        list[ModelInfo]: The list with all the models and they infos.
    """
    # Check if the file to open the llama server exist
    llama_exe_path: Path = ROOT_DIR / LLAMA_SERVER_DIR / LLAMA_SERVER_EXE
    if not llama_exe_path.is_file():
        return []

    llama_models: list[ str ] = []
    llama_models_path: Path = ROOT_DIR / LLAMA_MODELS_DIR
    if llama_models_path.is_dir():
        for model_file in llama_models_path.iterdir():
            # Get only the gguf files
            if model_file.suffix != ".gguf":
                continue

            # Keep non-split models
            if "-of-" not in model_file.name:
                llama_models.append( model_file.name )
                continue

            # Keep only the first part of split models
            if re.search( r"-00001-of-\d+\.gguf$", model_file.name ):
                llama_models.append( model_file.name )

    if llama_models == []:
        return []

    return [
        ModelInfo(
            label=f'{ re.sub( r"-00001-of-\d+$", "", model_name.replace(".gguf", "" ) ) } [llama-server]',
            name=model_name,
            source="llama-server"
        ) for model_name in sorted( llama_models )
    ]


def get_akkodis_models() -> list[ ModelInfo ]:
    """Get all the models available with AKKODIS acces.

    Returns:
        list[ModelInfo]: The list with all the models and they infos.
    """
    try:
        # Check if an AKKODIS openAI key exist
        get_akkodis_openai_api_key()

        return [
            ModelInfo( label=f"{ model_name } [AKKODIS]", name=model_name, source="akkodis" )
            for model_name in AKKODIS_MODELS
        ]

    except ImportError:
        return []


def get_models() -> list[ ModelInfo ]:
    """Return all available models across all backends.

    Returns:
        list[ModelInfo]: The list with all the models and they infos.
    """
    return get_akkodis_models() + get_llama_models()
