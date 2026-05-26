from __future__ import annotations

import json
from base64 import urlsafe_b64decode, urlsafe_b64encode

import pandas as pd
import streamlit as st

from src.inference import analyze_profile


_NUMERIC_KEYS = {
    "Age",
    "Screen_Time",
    "Social_Media_Hours",
    "Gaming_Hours",
    "Work_Study_Hours",
    "Sleep_Hours",
    "Notifications_Per_Day",
    "Physical_Activity_Score",
    "Caffeine_Intake",
}


def _encode_profile(inputs: dict[str, object]) -> str:
    payload = json.dumps(inputs, separators=(",", ":"), default=str)
    return urlsafe_b64encode(payload.encode("utf-8")).decode("ascii")


def _decode_profile(token: str) -> dict[str, object] | None:
    try:
        raw = urlsafe_b64decode(token.encode("ascii")).decode("utf-8")
        data = json.loads(raw)
        if not isinstance(data, dict):
            return None
        for key in _NUMERIC_KEYS:
            if key in data:
                data[key] = float(data[key])
        return data
    except Exception:
        return None


def share_url(inputs: dict[str, object]) -> str:
    """Build a relative URL fragment that re-opens the same profile."""
    return f"?p={_encode_profile(inputs)}"


def _hydrate_from_query_params(metadata: dict[str, object]) -> dict[str, object] | None:
    try:
        token = st.query_params.get("p")
    except Exception:
        token = None
    if not token:
        return None
    decoded = _decode_profile(token)
    if not decoded:
        return None
    merged = dict(metadata["defaults"])
    merged.update(decoded)
    return merged


def ensure_baseline(metadata: dict[str, object], reference: pd.DataFrame) -> dict[str, object]:
    """Make subpages safe even when opened directly without visiting Home first.

    Also hydrates profile state from the ?p=... query parameter (Share Profile link).
    """
    if "baseline_inputs" not in st.session_state:
        from_url = _hydrate_from_query_params(metadata)
        st.session_state.baseline_inputs = from_url or dict(metadata["defaults"])
    if "analysis" not in st.session_state:
        st.session_state.analysis = analyze_profile(
            st.session_state.baseline_inputs, reference
        )
    return st.session_state.analysis
