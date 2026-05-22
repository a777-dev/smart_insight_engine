from __future__ import annotations

from src import bootstrap  # noqa: F401

import streamlit as st

from src.charts import cluster_scatter
from src.config import CLUSTER_DESCRIPTIONS, CLUSTER_ICONS
from src.inference import load_artifacts, load_reference_dataset
from src.session import ensure_baseline
from src.styles import apply_styles, archetype_card, hero, insight_chip


st.set_page_config(page_title="Behavioral Archetypes", layout="wide")
apply_styles()

artifacts = load_artifacts()
reference = load_reference_dataset()
analysis = ensure_baseline(artifacts["metadata"], reference)

PLOTLY_CONFIG = {"responsive": True, "displayModeBar": False}

st.markdown(
    hero(
        eyebrow="Page 05",
        title="Behavioral Archetypes.",
        body="KMeans clustering reveals five behavioral personas across the unified dataset. Each archetype has a fingerprint and a recovery story.",
    ),
    unsafe_allow_html=True,
)

cluster = analysis["cluster"]
st.markdown(
    insight_chip(
        f"<strong>Your archetype.</strong> {cluster['label']} — {cluster['description']}",
        tone="warning" if cluster["label"] in {"Burnout Users", "Hyper-Connected Users"} else "default",
    ),
    unsafe_allow_html=True,
)

st.plotly_chart(cluster_scatter(reference), width="stretch", config=PLOTLY_CONFIG)

st.markdown("## Archetype Library")
for label, description in CLUSTER_DESCRIPTIONS.items():
    icon = CLUSTER_ICONS.get(label, "??")
    st.markdown(archetype_card(icon, label, description), unsafe_allow_html=True)

st.markdown("## Cluster Centroids")
centers = artifacts["metadata"]["cluster_centers"]
label_map = artifacts["metadata"]["cluster_labels"]
for cluster_id, values in centers.items():
    label = label_map.get(str(cluster_id)) or label_map.get(cluster_id, "Cluster")
    body = ", ".join(f"{key}: {float(val):.2f}" for key, val in values.items())
    st.markdown(
        insight_chip(f"<strong>{label}.</strong> {body}"),
        unsafe_allow_html=True,
    )
