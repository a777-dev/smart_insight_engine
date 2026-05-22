from __future__ import annotations

from src import bootstrap  # noqa: F401

import streamlit as st

from src.charts import gauge, radar_chart
from src.config import PALETTE
from src.inference import analyze_profile, load_artifacts, load_reference_dataset
from src.session import ensure_baseline
from src.styles import apply_styles, hero, insight_chip, metric_card
from src.training import ensure_artifacts


st.set_page_config(
    page_title="Home - Behavioral Intelligence Advisor",
    page_icon="BI",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_styles()

with st.spinner("Loading behavioral intelligence models..."):
    ensure_artifacts()
    artifacts = load_artifacts()
    reference = load_reference_dataset()

metadata = artifacts["metadata"]
ensure_baseline(metadata, reference)

st.markdown(
    hero(
        eyebrow="Region-Aware Behavioral Risk Prediction",
        title="Decode your digital lifestyle.",
        body=(
            f"This research-grade behavioral intelligence platform integrates "
            f"{metadata['dataset_summary']['rows']:,} multi-source records across India, USA, "
            "and Global cohorts. Predict stress, addiction, and productivity. Explain the why. "
            "Simulate a healthier you."
        ),
    ),
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div style="margin: 0.2rem 0 1.4rem 0;">
      <span class="pill primary">Stress</span>
      <span class="pill secondary">Addiction</span>
      <span class="pill accent">Productivity</span>
      <span class="pill">Region-Aware</span>
      <span class="pill">Explainable AI</span>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("## Your Profile")
st.caption("Move the sliders. The full multi-page advisor reads from this profile.")

defaults = metadata["defaults"]
options = metadata["options"]

with st.expander("Demographics", expanded=False):
    demo_cols = st.columns(2)
    with demo_cols[0]:
        age = st.slider("Age", 13, 80, int(defaults["Age"]), key="input_age")
        gender = st.selectbox(
            "Gender",
            options["Gender"],
            index=options["Gender"].index(defaults["Gender"])
            if defaults["Gender"] in options["Gender"]
            else 0,
            key="input_gender",
        )
    with demo_cols[1]:
        user_type = st.selectbox(
            "User Type",
            options["User_Type"],
            index=options["User_Type"].index(defaults.get("User_Type", "Mixed")),
            key="input_user_type",
        )
        region_group = st.selectbox(
            "Region",
            options["Region_Group"],
            index=options["Region_Group"].index(defaults.get("Region_Group", "Global")),
            key="input_region",
        )

slider_cols = st.columns(2)
with slider_cols[0]:
    screen_time = st.slider(
        "Screen Time (h/day)", 0.0, 14.0, float(defaults["Screen_Time"]), 0.1,
        key="input_screen",
    )
    social_media = st.slider(
        "Social Media Hours", 0.0, 8.0, float(defaults["Social_Media_Hours"]), 0.1,
        key="input_social",
    )
    gaming = st.slider(
        "Gaming Hours", 0.0, 6.0, float(defaults["Gaming_Hours"]), 0.1,
        key="input_gaming",
    )
    work_study = st.slider(
        "Work / Study Hours", 0.0, 10.0, float(defaults["Work_Study_Hours"]), 0.1,
        key="input_work",
    )

with slider_cols[1]:
    sleep = st.slider(
        "Sleep Hours", 2.0, 11.0, float(defaults["Sleep_Hours"]), 0.1, key="input_sleep"
    )
    notifications = st.slider(
        "Notifications / Day", 0.0, 250.0, float(defaults["Notifications_Per_Day"]), 5.0,
        key="input_notifications",
    )
    activity = st.slider(
        "Physical Activity (1-5)", 1.0, 5.0, float(defaults["Physical_Activity_Score"]), 0.1,
        key="input_activity",
    )
    caffeine = st.slider(
        "Caffeine Intake (mg)", 0.0, 350.0, float(defaults["Caffeine_Intake"]), 5.0,
        key="input_caffeine",
    )

age_group = (
    "Teen" if age < 20
    else "Young Adult" if age < 35
    else "Adult" if age < 55
    else "Older Adult"
)

submitted = st.button("Analyze My Lifestyle", width="stretch")

if submitted:
    inputs = {
        "Age": age,
        "Gender": gender,
        "User_Type": user_type,
        "Region_Group": region_group,
        "Age_Group": age_group,
        "Screen_Time": screen_time,
        "Social_Media_Hours": social_media,
        "Gaming_Hours": gaming,
        "Work_Study_Hours": work_study,
        "Sleep_Hours": sleep,
        "Notifications_Per_Day": notifications,
        "Physical_Activity_Score": activity,
        "Caffeine_Intake": caffeine,
    }
    st.session_state.baseline_inputs = inputs
    st.session_state.analysis = analyze_profile(inputs, reference)
    st.rerun()

analysis = st.session_state.analysis

st.markdown(
    insight_chip(f"<strong>Current read.</strong> {analysis['headline']}"),
    unsafe_allow_html=True,
)

for warning in analysis["warnings"]:
    st.markdown(insight_chip(warning, tone="danger"), unsafe_allow_html=True)

st.markdown("## Behavioral Overview")

metric_cols = st.columns(2)
metric_cols[0].markdown(
    metric_card(
        "Stress Level",
        f"{analysis['stress_level']:.2f}",
        delta=f"{analysis['stress_pct']:.0f}% of max",
        accent="primary",
    ),
    unsafe_allow_html=True,
)
metric_cols[1].markdown(
    metric_card(
        "Addiction Risk",
        analysis["addiction"]["label"],
        delta=f"severity {analysis['addiction']['severity']:.2f}",
        accent="warning" if analysis["addiction"]["label"] != "Low" else "secondary",
    ),
    unsafe_allow_html=True,
)

metric_cols_b = st.columns(2)
metric_cols_b[0].markdown(
    metric_card(
        "Productivity",
        f"{analysis['productivity']['productivity_score']*100:.0f}/100",
        delta=f"impact prob. {analysis['productivity']['impact_probability']:.2f}",
        accent="secondary",
    ),
    unsafe_allow_html=True,
)
metric_cols_b[1].markdown(
    metric_card(
        "Behavioral Risk Index",
        f"{analysis['behavioral_risk_index']:.2f}",
        delta=f"Lifestyle score {analysis['lifestyle_score']['total']:.0f}/100",
        accent="danger" if analysis["behavioral_risk_index"] > 0.45 else "accent",
    ),
    unsafe_allow_html=True,
)

st.markdown("## Lifestyle Gauges")
gauge_cols = st.columns(3)
gauge_cols[0].plotly_chart(
    gauge(
        "Predicted Stress",
        analysis["stress_level"],
        0.0,
        1.0,
        accent=PALETTE["danger"] if analysis["stress_level"] >= 0.55 else PALETTE["accent"],
    ),
    width="stretch",
    config={"responsive": True, "displayModeBar": False},
)
gauge_cols[1].plotly_chart(
    gauge(
        "Productivity Outlook",
        analysis["productivity"]["productivity_score"],
        0.0,
        1.0,
        accent=PALETTE["secondary"],
    ),
    width="stretch",
    config={"responsive": True, "displayModeBar": False},
)
gauge_cols[2].plotly_chart(
    gauge(
        "Behavioral Risk Index",
        analysis["behavioral_risk_index"],
        0.0,
        1.0,
        accent=PALETTE["primary"],
    ),
    width="stretch",
    config={"responsive": True, "displayModeBar": False},
)

st.markdown("## Lifestyle Balance vs Cohort")
st.plotly_chart(
    radar_chart(analysis["radar"]),
    width="stretch",
    config={"responsive": True, "displayModeBar": False},
)

st.markdown(
    """
    <div class="footer-note">
      Use the left-side navigation to explore the full advisor:
      <strong>Region-Aware Analytics</strong>,
      <strong>Students vs Professionals</strong>,
      <strong>AI Risk Prediction</strong>,
      <strong>Behavioral Archetypes</strong>,
      <strong>Explainable AI</strong>,
      <strong>Scenario Simulation</strong>, and the
      <strong>Smart Insight Engine</strong>.
    </div>
    """,
    unsafe_allow_html=True,
)
