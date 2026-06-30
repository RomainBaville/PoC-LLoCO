# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

"""LLM client.

Implements the same philosophy as the original ask_openai_request:
- one function
- takes a prompt
- returns plain text
- backend is hidden from the caller

This version uses a local Qwen GGUF model via llama-server.
"""

import os

import requests

# --------------------------------------------------
# Configuration
# --------------------------------------------------

LLM_SERVER_URL = os.getenv(
    "LLM_SERVER_URL",
    "http://localhost:8080/v1/chat/completions"
)

LLM_MODEL_NAME = os.getenv(
    "LLM_MODEL_NAME",
    "Qwen2.5-7B-Instruct-Q8_0"
)


# --------------------------------------------------
# Public API (same idea as ask_openai_request)
# --------------------------------------------------

def ask_llm_request(prompt: str) -> str:
    """Send a prompt to the local LLM and return the response text.
    """
    payload = {
        "model": LLM_MODEL_NAME,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a professional optimization analyst. "
                    "You explain results clearly and concisely."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        "temperature": 0.2,
        "top_p": 0.9,
        "max_tokens": 800,
        "stream": False,
    }

    response = requests.post(
        LLM_SERVER_URL,
        json=payload,
        timeout=3600,
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"LLM request failed "
            f"({response.status_code}): {response.text}"
        )

    data = response.json()

    try:
        return data["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError) as e:
        raise RuntimeError(
            f"Unexpected LLM response format: {data}"
        ) from e
