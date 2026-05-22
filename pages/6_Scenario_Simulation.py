from __future__ import annotations

from src import bootstrap  # noqa: F401

import streamlit as st

from src.charts import before_after_chart
from src.inference import analyze_profile, load_artifacts, load_reference_dataset
from src.session import ensure_baseline
from src.styles import apply_styles, hero, insight_chip, metric_card


st.set_page_config(page_title="Scenario Simulation", layout="wide")
apply_styles()

artifacts = load_artifacts()
reference = load_reference_dataset()
baseline_analysis = ensure_baseline(artifacts["metadata"], reference)
baseline_inputs = st.session_state.baseline_inputs

PLOTLY_CONFIG = {"responsive": True, "displayModeBar": False}

st.markdown(
    hero(
        eyebrow="Page 07",
        title="Scenario Simulation Engine.",
        body="Move the sliders to ask the model what-if. Each change re-runs the stress, addiction, and productivity predictions in real time.",
    ),
    unsafe_allow_html=True,
)

if "sim_inputs" not in st.session_state:
    st.session_state.sim_inputs = dict(baseline_inputs)

sim_cols = st.columns(2)
with sim_cols[0]:
    sleep = st.slider(
        "Sleep Hours",
        2.0,
        11.0,
        float(st.session_state.sim_inputs["Sleep_Hours"]),
        0.1,
    )
    screen = st.slider(
        "Screen Time (h/day)",
        0.0,
        14.0,
        float(st.session_state.sim_inputs["Screen_Time"]),
        0.1,
    )
    social = st.slider(
        "Social Media Hours",
        0.0,
        8.0,
        float(st.session_state.sim_inputs["Social_Media_Hours"]),
        0.1,
    )
    notifications = st.slider(
        "Notifications / Day",
        0.0,
        250.0,
        float(st.session_state.sim_inputs["Notifications_Per_Day"]),
        5.0,
    )

with sim_cols[1]:
    activity = st.slider(
        "Physical Activity (1-5)",
        1.0,
        5.0,
        float(st.session_state.sim_inputs["Physical_Activity_Score"]),
        0.1,
    )
    caffeine = st.slider(
        "Caffeine Intake (mg)",
        0.0,
        350.0,
        float(st.session_state.sim_inputs["Caffeine_Intake"]),
        5.0,
    )
    gaming = st.slider(
        "Gaming Hours",
        0.0,
        6.0,
        float(st.session_state.sim_inputs["Gaming_Hours"]),
        0.1,
    )
    work = st.slider(
        "Work / Study Hours",
        0.0,
        10.0,
        float(st.session_state.sim_inputs["Work_Study_Hours"]),
        0.1,
    )

if st.button("Reset to Baseline", width="stretch"):
    st.session_state.sim_inputs = dict(baseline_inputs)
    st.rerun()

scenario_inputs = dict(baseline_inputs)
scenario_inputs.update(
    {
        "Sleep_Hours": sleep,
        "Screen_Time": screen,
        "Social_Media_Hours": social,
        "Notifications_Per_Day": notifications,
        "Physical_Activity_Score": activity,
        "Caffeine_Intake": caffeine,
        "Gaming_Hours": gaming,
        "Work_Study_Hours": work,
    }
)
st.session_state.sim_inputs = scenario_inputs
scenario = analyze_profile(scenario_inputs, reference)

delta_top = st.columns(2)
delta_top[0].markdown(
    metric_card(
        "Stress Δ",
        f"{(scenario['stress_level'] - baseline_analysis['stress_level']):+.3f}",
        delta=f"Now {scenario['stress_level']:.2f}",
        accent="primary",
    ),
    unsafe_allow_html=True,
)
delta_top[1].markdown(
    metric_card(
        "Addiction Δ",
        f"{(scenario['addiction']['severity'] - baseline_analysis['addiction']['severity']):+.3f}",
        delta=f"Predicted: {scenario['addiction']['label']}",
        accent="warning",
    ),
    unsafe_allow_html=True,
)

delta_bot = st.columns(2)
delta_bot[0].markdown(
    metric_card(
        "Productivity Δ",
        f"{(scenario['productivity']['productivity_score'] - baseline_analysis['productivity']['productivity_score']):+.3f}",
        delta=f"Now {scenario['productivity']['productivity_score']*100:.0f}/100",
        accent="secondary",
    ),
    unsafe_allow_html=True,
)
delta_bot[1].markdown(
    metric_card(
        "BRI Δ",
        f"{(scenario['behavioral_risk_index'] - baseline_analysis['behavioral_risk_index']):+.3f}",
        delta=f"Now {scenario['behavioral_risk_index']:.2f}",
        accent="danger"
        if scenario["behavioral_risk_index"] > baseline_analysis["behavioral_risk_index"]
        else "secondary",
    ),
    unsafe_allow_html=True,
)

st.plotly_chart(
    before_after_chart(baseline_analysis, scenario),
    width="stretch",
    config=PLOTLY_CONFIG,
)

if scenario["cluster"]["label"] != baseline_analysis["cluster"]["label"]:
    st.markdown(
        insight_chip(
            f"This scenario would shift your archetype from {baseline_analysis['cluster']['label']} "
            f"to {scenario['cluster']['label']}.",
            tone="warning",
        ),
        unsafe_allow_html=True,
    )

st.markdown("### Scenario Insights")
for insight in scenario["warnings"] or [scenario["headline"]]:
    st.markdown(insight_chip(insight), unsafe_allow_html=True)
