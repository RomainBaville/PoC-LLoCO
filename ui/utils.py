# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.

import io
import json
import zipfile
from typing import Dict, List

import streamlit as st

from llm.session_model import OptimizationSession
from llm.session_prompt import build_session_summary_prompt
from llm.client import ask_llm_request


def log_step(message: str):
    if "journey" not in st.session_state:
        st.session_state.journey = []
    st.session_state.journey.append(message)


def generate_ai_summary(session: OptimizationSession) -> str:
    prompt = build_session_summary_prompt(session)
    return ask_llm_request(prompt)


def build_results_zip(
    solution_rows: List[Dict[str, str]],
    ai_summary: str,
    metadata: Dict,
) -> bytes:
    buffer = io.BytesIO()

    with zipfile.ZipFile(buffer, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        if solution_rows:
            headers = solution_rows[0].keys()
            csv_content = ",".join(headers) + "\n"
            csv_content += "\n".join(
                ",".join(str(row[h]) for h in headers)
                for row in solution_rows
            )
            zf.writestr("solution.csv", csv_content)

        zf.writestr("ai_summary.txt", ai_summary)
        zf.writestr("metadata.json", json.dumps(metadata, indent=2))

    buffer.seek(0)
    return buffer.read()
