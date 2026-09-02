# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from collections.abc import Callable
from dataclasses import dataclass

from llm.client.akkodis_client import ask_akkodis_client
from llm.client.llama_client import ask_llama_client


@dataclass
class LLMClient:
    """The class with all the llm client that can be used.

    Args:
        key (str): The llm client.
        description (str): The description of the client.
        ask_fn (Callable[[str, str], str]): The function to ask the llm client.
    """
    key: str
    description: str
    ask_fn: Callable[ [ str, str ], str ]


CLIENTS = {
    "akkodis": LLMClient( key="akkodis", description="LLM client from akkodis servers.", ask_fn=ask_akkodis_client ),
    "llama-server":
    LLMClient( key="llama-server", description="LLM client from llama servers.", ask_fn=ask_llama_client )
}
