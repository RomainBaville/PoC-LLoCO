# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.

import streamlit as st

_CSS = """
<style>
/* ── Sidebar ─────────────────────────────────────── */
[data-testid="stSidebar"] {
    background-color: #F8FAFC;
    border-right: 1px solid #E2E8F0;
}
[data-testid="stSidebar"] section[data-testid="stSidebarContent"] {
    padding-top: 1.4rem;
    padding-bottom: 1.5rem;
}
[data-testid="stSidebar"] h2 {
    font-size: 1rem;
    font-weight: 700;
    color: #1E3A8A;
    margin-bottom: 0.2rem;
}

/* ── Section labels ──────────────────────────────── */
.ui-label {
    display: block;
    font-size: 0.65rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.09em;
    color: #94A3B8;
    margin: 1rem 0 0.25rem 0;
}

/* ── Divider ─────────────────────────────────────── */
.ui-hr {
    border: none;
    border-top: 1px solid #E2E8F0;
    margin: 0.75rem 0;
}

/* ── Journal entries ─────────────────────────────── */
.ui-journal {
    font-size: 0.74rem;
    color: #64748B;
    border-left: 2px solid #CBD5E1;
    padding: 0.08rem 0 0.08rem 0.55rem;
    margin-bottom: 0.2rem;
    line-height: 1.45;
}

/* ── AI result block ─────────────────────────────── */
.ui-ai {
    background: #F0F9FF;
    border-left: 3px solid #3B82F6;
    border-radius: 0 8px 8px 0;
    padding: 1rem 1.2rem;
    font-size: 0.91rem;
    line-height: 1.7;
    color: #1E293B;
    margin-top: 0.5rem;
}

/* ── Hero section ────────────────────────────────── */
.ui-hero-title {
    font-size: 1.9rem;
    font-weight: 700;
    color: #1E3A8A;
    line-height: 1.2;
    margin-bottom: 0.35rem;
}
.ui-hero-sub {
    font-size: 0.97rem;
    color: #64748B;
    margin-bottom: 1.6rem;
    font-weight: 400;
}

/* ── Metric cards ────────────────────────────────── */
[data-testid="stMetric"] {
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
    padding: 0.9rem 1.1rem;
}
[data-testid="stMetricLabel"] p {
    font-size: 0.72rem !important;
    font-weight: 700 !important;
    color: #94A3B8 !important;
    text-transform: uppercase;
    letter-spacing: 0.07em;
}
[data-testid="stMetricValue"] {
    font-size: 1.35rem !important;
    font-weight: 700 !important;
    color: #1E3A8A !important;
}

/* ── Onboarding placeholder ──────────────────────── */
.ui-hint {
    font-size: 0.85rem;
    color: #94A3B8;
    font-style: italic;
    margin-top: 1.5rem;
}

/* ── Model picker banner ─────────────────────────────────────────── */
.ui-model-banner {
    background: linear-gradient(135deg, #1E3A8A 0%, #2563EB 100%);
    border-radius: 10px;
    padding: 0.75rem 0.9rem;
    margin-bottom: 0.5rem;
}
.ui-model-banner-label {
    font-size: 0.62rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #93C5FD;
    margin: 0 0 0.3rem 0;
    display: block;
}
.ui-model-banner-value {
    font-size: 0.82rem;
    font-weight: 600;
    color: #FFFFFF;
}
.ui-model-banner-none {
    font-size: 0.8rem;
    color: #BFDBFE;
    font-style: italic;
}
</style>
"""


def inject():
    st.markdown(_CSS, unsafe_allow_html=True)


def section_label(text: str):
    st.markdown(f'<span class="ui-label">{text}</span>', unsafe_allow_html=True)


def divider():
    st.markdown('<hr class="ui-hr">', unsafe_allow_html=True)


def ai_block(content: str):
    st.markdown(f'<div class="ui-ai">{content}</div>', unsafe_allow_html=True)


def hero(title: str, subtitle: str = ""):
    html = f'<p class="ui-hero-title">{title}</p>'
    if subtitle:
        html += f'<p class="ui-hero-sub">{subtitle}</p>'
    st.markdown(html, unsafe_allow_html=True)
