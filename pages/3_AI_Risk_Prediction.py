from __future__ import annotations

from src import bootstrap  # noqa: F401

import streamlit as st

from src.charts import gauge
from src.config import PALETTE
from src.inference import load_artifacts, load_reference_dataset
from src.session import ensure_baseline
from src.styles import apply_styles, hero, insight_chip, metric_card


st.set_page_config(page_title="AI Risk Prediction", layout="wide")
apply_styles()

artifacts = load_artifacts()
metadata = artifacts["metadata"]
reference = load_reference_dataset()
analysis = ensure_baseline(metadata, reference)

PLOTLY_CONFIG = {"responsive": True, "displayModeBar": False}

st.markdown(
    hero(
        eyebrow="Page 04",
        title="AI Risk Prediction.",
        body=(
            "Three RandomForest models run on your profile to predict stress level, addiction "
            "category, and productivity impact. Evaluation metrics are reported on a held-out test set."
        ),
    ),
    unsafe_allow_html=True,
)

metrics = metadata["metrics"]
metric_row1 = st.columns(3)
metric_row1[0].markdown(
    metric_card(
        "Stress RMSE",
        f"{metrics['stress_rmse']:.3f}",
        delta="Lower is better",
        accent="primary",
    ),
    unsafe_allow_html=True,
)
metric_row1[1].markdown(
    metric_card(
        "Addiction Acc",
        f"{metrics['addiction_accuracy']*100:.1f}%",
        delta=f"F1 {metrics['addiction_f1']:.2f}",
        accent="warning",
    ),
    unsafe_allow_html=True,
)
metric_row1[2].markdown(
    metric_card(
        "Productivity Acc",
        f"{metrics['productivity_accuracy']*100:.1f}%",
        delta=f"F1 {metrics['productivity_f1']:.2f}",
        accent="secondary",
    ),
    unsafe_allow_html=True,
)

metric_row2 = st.columns(2)
metric_row2[0].markdown(
    metric_card(
        "Dataset",
        f"{metadata['dataset_summary']['rows']:,}",
        delta="multi-source records",
        accent="accent",
    ),
    unsafe_allow_html=True,
)
metric_row2[1].markdown(
    metric_card(
        "Algorithm",
        "RandomForest",
        delta="ensemble of decision trees",
        accent="primary",
    ),
    unsafe_allow_html=True,
)

st.markdown("## Live Prediction for Your Profile")
gauge_cols = st.columns(3)
gauge_cols[0].plotly_chart(
    gauge(
        "Stress",
        analysis["stress_level"],
        0.0,
        1.0,
        PALETTE["danger"] if analysis["stress_level"] >= 0.55 else PALETTE["accent"],
    ),
    width="stretch",
    config=PLOTLY_CONFIG,
)
gauge_cols[1].plotly_chart(
    gauge(
        "Addiction Severity",
        analysis["addiction"]["severity"],
        0.0,
        1.0,
        PALETTE["accent"],
    ),
    width="stretch",
    config=PLOTLY_CONFIG,
)
gauge_cols[2].plotly_chart(
    gauge(
        "Productivity Outlook",
        analysis["productivity"]["productivity_score"],
        0.0,
        1.0,
        PALETTE["secondary"],
    ),
    width="stretch",
    config=PLOTLY_CONFIG,
)

st.markdown("## Class Probabilities")
prob_cols = st.columns(2)
with prob_cols[0]:
    st.markdown("**Addiction Category Probabilities**")
    for label, value in analysis["addiction"]["probabilities"].items():
        st.markdown(
            insight_chip(
                f"<strong>{label}.</strong> {value*100:.1f}%",
                tone="danger" if label == "High" else "warning" if label == "Moderate" else "default",
            ),
            unsafe_allow_html=True,
        )

with prob_cols[1]:
    st.markdown("**Productivity Impact**")
    st.markdown(
        insight_chip(
            f"<strong>Impact Probability.</strong> {analysis['productivity']['impact_probability']*100:.1f}%"
        ),
        unsafe_allow_html=True,
    )
    st.markdown(
        insight_chip(
            f"<strong>Productivity Score.</strong> {analysis['productivity']['productivity_score']*100:.1f}/100"
        ),
        unsafe_allow_html=True,
    )

st.markdown(
    insight_chip(
        "Models trained with stratified 80/20 split, balanced class weights, and shared preprocessing pipeline.",
    ),
    unsafe_allow_html=True,
)
