from __future__ import annotations

from src import bootstrap  # noqa: F401

import streamlit as st

from src.charts import correlation_heatmap, feature_importance_bar, local_impact_chart
from src.config import CORRELATION_FIELDS
from src.inference import (
    load_artifacts,
    load_reference_dataset,
    local_feature_impacts,
)
from src.insights import build_explanations
from src.session import ensure_baseline
from src.styles import apply_styles, hero, insight_chip


st.set_page_config(page_title="Explainable AI Lab", layout="wide")
apply_styles()

artifacts = load_artifacts()
metadata = artifacts["metadata"]
reference = load_reference_dataset()
analysis = ensure_baseline(metadata, reference)

PLOTLY_CONFIG = {"responsive": True, "displayModeBar": False}

st.markdown(
    hero(
        eyebrow="Page 06",
        title="Explainable AI Lab.",
        body="Open the box. RandomForest feature importances tell us which signals matter most in aggregate, while local sensitivity reveals what is driving your prediction.",
    ),
    unsafe_allow_html=True,
)

impacts = local_feature_impacts(analysis["profile"])
explanations = build_explanations(impacts)

st.markdown("## Global Feature Importance")
importance_cols = st.columns(3)
with importance_cols[0]:
    st.plotly_chart(
        feature_importance_bar(metadata["feature_importance"]["stress"], "stress"),
        width="stretch",
        config=PLOTLY_CONFIG,
    )
with importance_cols[1]:
    st.plotly_chart(
        feature_importance_bar(metadata["feature_importance"]["addiction"], "addiction"),
        width="stretch",
        config=PLOTLY_CONFIG,
    )
with importance_cols[2]:
    st.plotly_chart(
        feature_importance_bar(
            metadata["feature_importance"]["productivity"], "productivity"
        ),
        width="stretch",
        config=PLOTLY_CONFIG,
    )

st.markdown("## Local Sensitivity For You")
st.caption(
    "Each bar shows the predicted change when that feature is nudged upward. "
    "Red increases the risk metric; green reduces it."
)
local_cols = st.columns(3)
with local_cols[0]:
    st.plotly_chart(local_impact_chart(impacts, "stress"), width="stretch", config=PLOTLY_CONFIG)
with local_cols[1]:
    st.plotly_chart(local_impact_chart(impacts, "addiction"), width="stretch", config=PLOTLY_CONFIG)
with local_cols[2]:
    st.plotly_chart(local_impact_chart(impacts, "productivity"), width="stretch", config=PLOTLY_CONFIG)

st.markdown("## Causal Explanation Cards")
exp_cols = st.columns(3)
exp_cols[0].markdown(
    insight_chip(f"<strong>Stress.</strong> {explanations['stress']}"),
    unsafe_allow_html=True,
)
exp_cols[1].markdown(
    insight_chip(f"<strong>Addiction.</strong> {explanations['addiction']}", tone="warning"),
    unsafe_allow_html=True,
)
exp_cols[2].markdown(
    insight_chip(f"<strong>Productivity.</strong> {explanations['productivity']}"),
    unsafe_allow_html=True,
)

st.markdown("## Correlation Map")
st.plotly_chart(
    correlation_heatmap(reference, CORRELATION_FIELDS),
    width="stretch",
    config=PLOTLY_CONFIG,
)
