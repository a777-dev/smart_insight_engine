from __future__ import annotations

from src import bootstrap  # noqa: F401

import streamlit as st

from src.analytics import (
    addiction_distribution,
    burnout_share,
    sleep_deficit_share,
    user_insight_cards,
    user_summary,
)
from src.charts import (
    addiction_distribution_chart,
    grouped_bar,
)
from src.config import USER_PALETTE
from src.inference import load_artifacts, load_reference_dataset
from src.session import ensure_baseline
from src.styles import apply_styles, hero, insight_chip, metric_card


st.set_page_config(page_title="Students vs Professionals", layout="wide")
apply_styles()

artifacts = load_artifacts()
dataset = load_reference_dataset()
ensure_baseline(artifacts["metadata"], dataset)

PLOTLY_CONFIG = {"responsive": True, "displayModeBar": False}

st.markdown(
    hero(
        eyebrow="Page 03",
        title="Students vs Professionals.",
        body="Mirror behavioral signatures across academic and workforce populations. Look for burnout, sleep deficit, and addiction differences.",
    ),
    unsafe_allow_html=True,
)

summary = user_summary(dataset).set_index("User_Type")

split = st.columns(2)


def render_segment(column, label: str, accent: str) -> None:
    if label not in summary.index:
        return
    row = summary.loc[label]
    with column:
        st.markdown(
            f"<h3 style='margin: 0.2rem 0 0.6rem 0;'>{label}s</h3>",
            unsafe_allow_html=True,
        )
        st.markdown(
            metric_card(
                "Avg Screen Time",
                f"{row['Screen_Time']:.1f} h",
                delta=f"Social media {row['Social_Media_Hours']:.1f} h",
                accent=accent,
            ),
            unsafe_allow_html=True,
        )
        st.markdown(
            metric_card(
                "Avg Sleep",
                f"{row['Sleep_Hours']:.1f} h",
                delta=f"Activity {row['Physical_Activity_Score']:.1f}/5",
                accent=accent,
            ),
            unsafe_allow_html=True,
        )
        st.markdown(
            metric_card(
                "Stress (norm)",
                f"{row['Stress_Level_Norm']:.2f}",
                delta=f"BRI {row['Behavioral_Risk_Index_Recomputed']:.2f}",
                accent=accent,
            ),
            unsafe_allow_html=True,
        )


render_segment(split[0], "Student", "primary")
render_segment(split[1], "Professional", "warning")

st.markdown("### Behavioral Comparison")
palette = {
    "Screen_Time": USER_PALETTE["Student"],
    "Sleep_Hours": USER_PALETTE["Mixed"],
    "Stress_Level_Norm": USER_PALETTE["Professional"],
    "Physical_Activity_Score": USER_PALETTE["Mixed"],
    "Work_Study_Hours": USER_PALETTE["Student"],
    "Social_Media_Hours": USER_PALETTE["Professional"],
    "Notifications_Per_Day": USER_PALETTE["Professional"],
    "Addiction_Level_Norm": USER_PALETTE["Student"],
    "Behavioral_Risk_Index_Recomputed": USER_PALETTE["Professional"],
}

st.plotly_chart(
    grouped_bar(
        user_summary(dataset),
        "User_Type",
        ["Screen_Time", "Sleep_Hours", "Work_Study_Hours", "Social_Media_Hours"],
        palette,
        "Lifestyle Hours by User Type",
    ),
    width="stretch",
    config=PLOTLY_CONFIG,
)

burnout = burnout_share(dataset, "User_Type")
deficit = sleep_deficit_share(dataset, "User_Type")
metrics_cols = st.columns(3)
for index, row in burnout.iterrows():
    metrics_cols[index % 3].markdown(
        insight_chip(
            f"<strong>{row['User_Type']}.</strong> {row['burnout_share']*100:.1f}% sit in the high-stress band.",
            tone="warning",
        ),
        unsafe_allow_html=True,
    )

for index, row in deficit.iterrows():
    metrics_cols[index % 3].markdown(
        insight_chip(
            f"<strong>{row['User_Type']}.</strong> {row['deficit_share']*100:.1f}% sleep below 6h.",
            tone="danger",
        ),
        unsafe_allow_html=True,
    )

st.markdown("### Addiction Patterns")
addiction_share = addiction_distribution(dataset, "User_Type")
st.plotly_chart(
    addiction_distribution_chart(
        addiction_share, "User_Type", "Addiction Category Share by User Type"
    ),
    width="stretch",
    config=PLOTLY_CONFIG,
)

st.markdown("### Behavioral Differences")
for card in user_insight_cards(dataset):
    st.markdown(
        insight_chip(f"<strong>{card['title']}.</strong> {card['body']}"),
        unsafe_allow_html=True,
    )
