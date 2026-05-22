from __future__ import annotations

from src import bootstrap  # noqa: F401

import streamlit as st

from src.inference import load_artifacts, load_reference_dataset
from src.insights import generate_insights
from src.session import ensure_baseline
from src.styles import apply_styles, hero, insight_chip, metric_card


st.set_page_config(page_title="Smart Insight Engine", layout="wide")
apply_styles()

artifacts = load_artifacts()
reference = load_reference_dataset()
analysis = ensure_baseline(artifacts["metadata"], reference)

st.markdown(
    hero(
        eyebrow="Page 08",
        title="Smart Insight Engine.",
        body="Personalized, rule-based and model-aware recommendations. Three to five actions that move the lifestyle score upward.",
    ),
    unsafe_allow_html=True,
)

st.markdown("## Snapshot")
snap_top = st.columns(2)
snap_top[0].markdown(
    metric_card(
        "Lifestyle Score",
        f"{analysis['lifestyle_score']['total']:.0f}/100",
        delta=analysis["headline"],
        accent="primary",
    ),
    unsafe_allow_html=True,
)

components = analysis["lifestyle_score"]["components"]
component_items = list(components.items())
snap_top[1].markdown(
    metric_card(
        component_items[0][0],
        f"{component_items[0][1]:.0f}",
        accent="secondary" if component_items[0][1] >= 60
        else "warning" if component_items[0][1] >= 40
        else "danger",
    ),
    unsafe_allow_html=True,
)

snap_bot = st.columns(3)
for index, (name, value) in enumerate(component_items[1:]):
    snap_bot[index % 3].markdown(
        metric_card(
            name,
            f"{value:.0f}",
            accent="secondary" if value >= 60 else "warning" if value >= 40 else "danger",
        ),
        unsafe_allow_html=True,
    )

st.markdown("## Recommended Actions")
insights = generate_insights(
    profile=analysis["profile"],
    stress_norm=analysis["stress_level"],
    productivity_score=analysis["productivity"]["productivity_score"],
    addiction_label=analysis["addiction"]["label"],
    behavioral_risk_index=analysis["behavioral_risk_index"],
    cluster_label=analysis["cluster"]["label"],
)
for index, message in enumerate(insights, start=1):
    tone = "warning" if "burnout" in message.lower() or "high" in message.lower() else "default"
    st.markdown(
        insight_chip(f"<strong>Action {index}.</strong> {message}", tone=tone),
        unsafe_allow_html=True,
    )

st.markdown("## How These Are Generated")
st.markdown(
    insight_chip(
        "Insights blend explicit rules (sleep, screen, social media thresholds) with model outputs "
        "(stress regression, addiction classifier, productivity classifier). The engine returns the "
        "top five highest-impact actions for your current profile."
    ),
    unsafe_allow_html=True,
)
