from __future__ import annotations

from src import bootstrap  # noqa: F401

import streamlit as st

from src.analytics import (
    addiction_distribution,
    region_insight_cards,
    region_summary,
    sleep_deficit_share,
)
from src.charts import (
    addiction_distribution_chart,
    grouped_bar,
    violin_by_region,
)
from src.config import REGION_PALETTE
from src.inference import load_artifacts, load_reference_dataset
from src.session import ensure_baseline
from src.styles import apply_styles, hero, insight_chip


st.set_page_config(page_title="Region-Aware Analytics", layout="wide")
apply_styles()

artifacts = load_artifacts()
dataset = load_reference_dataset()
ensure_baseline(artifacts["metadata"], dataset)

PLOTLY_CONFIG = {"responsive": True, "displayModeBar": False}

st.markdown(
    hero(
        eyebrow="Page 02",
        title="Region-Aware Analytics.",
        body="Compare India, USA, and Global cohorts on stress, sleep, screen time, social media intensity, and addiction patterns.",
    ),
    unsafe_allow_html=True,
)

summary = region_summary(dataset)

palette = {
    "Screen_Time": REGION_PALETTE["India"],
    "Social_Media_Hours": REGION_PALETTE["USA"],
    "Sleep_Hours": REGION_PALETTE["Global"],
}

st.plotly_chart(
    grouped_bar(
        summary,
        "Region_Group",
        ["Screen_Time", "Social_Media_Hours", "Sleep_Hours"],
        palette,
        "Digital Lifestyle Averages by Region",
    ),
    width="stretch",
    config=PLOTLY_CONFIG,
)

st.markdown("### Stress, Addiction, and Notification Patterns")
chart_cols = st.columns(2)
with chart_cols[0]:
    st.plotly_chart(
        violin_by_region(dataset, "Stress_Level_Norm", "Stress Distribution by Region"),
        width="stretch",
        config=PLOTLY_CONFIG,
    )
with chart_cols[1]:
    st.plotly_chart(
        violin_by_region(
            dataset, "Notifications_Per_Day", "Notifications/Day by Region"
        ),
        width="stretch",
        config=PLOTLY_CONFIG,
    )

st.markdown("### Addiction Category Composition")
addiction_share = addiction_distribution(dataset, "Region_Group")
st.plotly_chart(
    addiction_distribution_chart(
        addiction_share, "Region_Group", "Addiction Category Share by Region"
    ),
    width="stretch",
    config=PLOTLY_CONFIG,
)

st.markdown("### Sleep Deficit Share")
deficit = sleep_deficit_share(dataset, "Region_Group")
deficit_cols = st.columns(3)
for index, row in deficit.iterrows():
    deficit_cols[index % 3].markdown(
        insight_chip(
            f"<strong>{row['Region_Group']}.</strong> "
            f"{row['deficit_share']*100:.1f}% of users sleep below 6 hours.",
            tone="warning",
        ),
        unsafe_allow_html=True,
    )

st.markdown("### Regional Insight Cards")
cards = region_insight_cards(dataset)
card_cols = st.columns(len(cards) if cards else 1)
for column, card in zip(card_cols, cards):
    column.markdown(
        insight_chip(f"<strong>{card['title']}.</strong> {card['body']}"),
        unsafe_allow_html=True,
    )
