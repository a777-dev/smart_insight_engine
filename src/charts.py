from __future__ import annotations

from typing import Iterable

import pandas as pd
import plotly.graph_objects as go

from src.config import (
    ADDICTION_PALETTE,
    PALETTE,
    REGION_PALETTE,
    USER_PALETTE,
    UI_FIELD_LABELS,
)


FONT = "Outfit, ui-sans-serif, system-ui, sans-serif"


def _flat_layout(
    fig: go.Figure,
    height: int = 320,
    *,
    has_legend: bool = False,
    has_title: bool = True,
) -> go.Figure:
    top_margin = 64 if has_title else 28
    bottom_margin = 80 if has_legend else 32
    fig.update_layout(
        paper_bgcolor=PALETTE["background"],
        plot_bgcolor=PALETTE["background"],
        font=dict(family=FONT, color=PALETTE["foreground"], size=13),
        margin=dict(l=16, r=16, t=top_margin, b=bottom_margin),
        height=height + (40 if has_legend else 0),
        autosize=True,
        hoverlabel=dict(
            bgcolor=PALETTE["foreground"],
            font=dict(color=PALETTE["background"], family=FONT),
        ),
    )
    if has_legend:
        fig.update_layout(
            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.18,
                xanchor="center",
                x=0.5,
                font=dict(size=12, family=FONT),
                bgcolor="rgba(0,0,0,0)",
            )
        )
    fig.update_xaxes(
        showgrid=True,
        gridcolor=PALETTE["border"],
        gridwidth=1,
        zerolinecolor=PALETTE["border"],
        linecolor=PALETTE["border"],
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor=PALETTE["border"],
        gridwidth=1,
        zerolinecolor=PALETTE["border"],
        linecolor=PALETTE["border"],
    )
    return fig


def _title(text: str) -> dict:
    return dict(
        text=text,
        font=dict(size=16, color=PALETTE["foreground"], family=FONT),
        x=0.0,
        xanchor="left",
        y=0.97,
        yanchor="top",
        pad=dict(b=8),
    )


def gauge(title: str, value: float, minimum: float, maximum: float, accent: str) -> go.Figure:
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            number=dict(font=dict(size=42, color=PALETTE["foreground"], family=FONT)),
            gauge=dict(
                axis=dict(range=[minimum, maximum], tickcolor=PALETTE["foreground"]),
                bar=dict(color=accent, thickness=0.32),
                bgcolor=PALETTE["muted"],
                borderwidth=0,
                steps=[
                    dict(range=[minimum, minimum + (maximum - minimum) * 0.5], color=PALETTE["muted"]),
                    dict(range=[minimum + (maximum - minimum) * 0.5, maximum], color="#E5E7EB"),
                ],
            ),
            domain={"x": [0, 1], "y": [0, 1]},
            title=dict(text=title, font=dict(size=14, color=PALETTE["soft_text"], family=FONT)),
        )
    )
    return _flat_layout(fig, height=260, has_legend=False, has_title=False)


def donut(title: str, labels: Iterable[str], values: Iterable[float], colors: Iterable[str]) -> go.Figure:
    fig = go.Figure(
        go.Pie(
            labels=list(labels),
            values=list(values),
            hole=0.62,
            marker=dict(colors=list(colors), line=dict(color=PALETTE["background"], width=2)),
            textinfo="label+percent",
            textfont=dict(family=FONT, color=PALETTE["foreground"]),
        )
    )
    fig.update_layout(title=_title(title))
    return _flat_layout(fig, height=320, has_legend=True)


def grouped_bar(
    frame: pd.DataFrame,
    category: str,
    metrics: list[str],
    palette: dict[str, str],
    title: str,
) -> go.Figure:
    fig = go.Figure()
    for metric in metrics:
        fig.add_bar(
            x=frame[category].astype(str).tolist(),
            y=frame[metric].astype(float).tolist(),
            name=UI_FIELD_LABELS.get(metric, metric),
            marker_color=palette.get(metric, PALETTE["primary"]),
            text=[f"{v:.2f}" for v in frame[metric].astype(float)],
            textposition="outside",
        )
    fig.update_layout(barmode="group", title=_title(title))
    return _flat_layout(fig, height=380, has_legend=True)


def stacked_share(
    frame: pd.DataFrame, category: str, value: str, group: str, palette: dict[str, str], title: str
) -> go.Figure:
    fig = go.Figure()
    for level in frame[group].unique().tolist():
        sub = frame[frame[group] == level]
        fig.add_bar(
            x=sub[category].astype(str).tolist(),
            y=sub[value].astype(float).tolist(),
            name=str(level),
            marker_color=palette.get(level, PALETTE["primary"]),
            text=[f"{v:.1f}%" for v in sub[value].astype(float)],
            textposition="inside",
        )
    fig.update_layout(barmode="stack", title=_title(title))
    return _flat_layout(fig, height=380, has_legend=True)


def violin_by_region(dataset: pd.DataFrame, metric: str, title: str) -> go.Figure:
    fig = go.Figure()
    for region, color in REGION_PALETTE.items():
        subset = dataset[dataset["Region_Group"] == region]
        if subset.empty:
            continue
        fig.add_trace(
            go.Violin(
                x=[region] * len(subset),
                y=subset[metric].astype(float),
                name=region,
                line_color=color,
                fillcolor=color,
                opacity=0.55,
                box_visible=True,
                meanline_visible=True,
            )
        )
    fig.update_layout(title=_title(title), showlegend=False)
    return _flat_layout(fig, height=380, has_legend=False)


def correlation_heatmap(dataset: pd.DataFrame, columns: list[str]) -> go.Figure:
    matrix = dataset[columns].corr().round(2)
    fig = go.Figure(
        go.Heatmap(
            z=matrix.values,
            x=[UI_FIELD_LABELS.get(c, c) for c in columns],
            y=[UI_FIELD_LABELS.get(c, c) for c in columns],
            colorscale=[(0, PALETTE["primary"]), (0.5, PALETTE["background"]), (1, PALETTE["accent"])],
            zmid=0,
            text=matrix.values,
            texttemplate="%{text:.2f}",
            colorbar=dict(thickness=14),
        )
    )
    fig.update_layout(title=_title("Behavioral Correlation Map"))
    return _flat_layout(fig, height=520, has_legend=False)


def feature_importance_bar(importances: dict[str, float], target: str) -> go.Figure:
    items = list(importances.items())[:8]
    labels = [UI_FIELD_LABELS.get(name, name) for name, _ in items][::-1]
    values = [value for _, value in items][::-1]
    fig = go.Figure(
        go.Bar(
            x=values,
            y=labels,
            orientation="h",
            marker_color=PALETTE["primary"]
            if target == "stress"
            else PALETTE["accent"]
            if target == "addiction"
            else PALETTE["secondary"],
            text=[f"{v:.2%}" for v in values],
            textposition="outside",
        )
    )
    fig.update_layout(
        title=_title(f"Feature Importance - {target.title()}"),
        xaxis=dict(tickformat=".0%"),
    )
    return _flat_layout(fig, height=400, has_legend=False)


def local_impact_chart(impacts: dict[str, dict[str, float]], target: str) -> go.Figure:
    rows = sorted(impacts.items(), key=lambda item: abs(item[1].get(target, 0.0)), reverse=True)
    labels = [UI_FIELD_LABELS.get(name, name) for name, _ in rows][::-1]
    values = [item[1].get(target, 0.0) for item in rows][::-1]
    colors = [PALETTE["danger"] if v > 0 else PALETTE["secondary"] for v in values]
    fig = go.Figure(
        go.Bar(
            x=values,
            y=labels,
            orientation="h",
            marker_color=colors,
            text=[f"{v:+.3f}" for v in values],
            textposition="outside",
        )
    )
    fig.update_layout(
        title=_title(f"Local Sensitivity - {target.title()}"),
        xaxis=dict(zeroline=True, zerolinecolor=PALETTE["foreground"]),
    )
    return _flat_layout(fig, height=400, has_legend=False)


def radar_chart(payload: dict[str, list[float]]) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Scatterpolar(
            r=payload["user"] + [payload["user"][0]],
            theta=payload["axes"] + [payload["axes"][0]],
            fill="toself",
            name="You",
            line=dict(color=PALETTE["primary"], width=3),
            fillcolor="rgba(59,130,246,0.18)",
        )
    )
    fig.add_trace(
        go.Scatterpolar(
            r=payload["average"] + [payload["average"][0]],
            theta=payload["axes"] + [payload["axes"][0]],
            fill="toself",
            name="Cohort Average",
            line=dict(color=PALETTE["accent"], width=2, dash="dot"),
            fillcolor="rgba(245,158,11,0.10)",
        )
    )
    fig.update_layout(
        polar=dict(
            bgcolor=PALETTE["background"],
            radialaxis=dict(visible=True, range=[0, 100], gridcolor=PALETTE["border"]),
            angularaxis=dict(gridcolor=PALETTE["border"]),
        ),
        title=_title("Lifestyle Balance"),
    )
    return _flat_layout(fig, height=440, has_legend=True)


def percentile_chart(percentiles: dict[str, float]) -> go.Figure:
    labels = [UI_FIELD_LABELS.get(k, k) for k in percentiles.keys()]
    values = list(percentiles.values())
    fig = go.Figure(
        go.Bar(
            x=values,
            y=labels,
            orientation="h",
            marker_color=PALETTE["primary"],
            text=[f"{v:.0f}th" for v in values],
            textposition="outside",
        )
    )
    fig.update_layout(
        title=_title("Where You Sit vs Cohort"),
        xaxis=dict(range=[0, 100], ticksuffix="%"),
    )
    return _flat_layout(fig, height=340, has_legend=False)


def before_after_chart(baseline: dict[str, object], scenario: dict[str, object]) -> go.Figure:
    metrics = ["Stress", "Addiction Severity", "Productivity", "BRI", "Lifestyle"]
    base_values = [
        baseline["stress_level"] * 100,
        baseline["addiction"]["severity"] * 100,
        baseline["productivity"]["productivity_score"] * 100,
        baseline["behavioral_risk_index"] * 100,
        baseline["lifestyle_score"]["total"],
    ]
    scenario_values = [
        scenario["stress_level"] * 100,
        scenario["addiction"]["severity"] * 100,
        scenario["productivity"]["productivity_score"] * 100,
        scenario["behavioral_risk_index"] * 100,
        scenario["lifestyle_score"]["total"],
    ]
    fig = go.Figure()
    fig.add_bar(
        x=metrics,
        y=base_values,
        name="Current",
        marker_color=PALETTE["accent"],
        text=[f"{v:.0f}" for v in base_values],
        textposition="outside",
    )
    fig.add_bar(
        x=metrics,
        y=scenario_values,
        name="Scenario",
        marker_color=PALETTE["primary"],
        text=[f"{v:.0f}" for v in scenario_values],
        textposition="outside",
    )
    fig.update_layout(barmode="group", title=_title("Before vs After"))
    return _flat_layout(fig, height=380, has_legend=True)


def cluster_scatter(dataset: pd.DataFrame, sample_size: int = 4000) -> go.Figure:
    frame = dataset.sample(min(sample_size, len(dataset)), random_state=42)
    fig = go.Figure()
    for label in frame["Cluster_Label"].dropna().unique():
        subset = frame[frame["Cluster_Label"] == label]
        fig.add_trace(
            go.Scatter(
                x=subset["Screen_Time"],
                y=subset["Sleep_Hours"],
                mode="markers",
                name=label,
                marker=dict(size=7, opacity=0.55),
                text=subset["Cluster_Label"],
            )
        )
    fig.update_layout(
        title=_title("Cluster Constellation (Screen vs Sleep)"),
        xaxis_title="Screen Time (h/day)",
        yaxis_title="Sleep Hours",
    )
    return _flat_layout(fig, height=500, has_legend=True)


def addiction_distribution_chart(frame: pd.DataFrame, category: str, title: str) -> go.Figure:
    fig = go.Figure()
    for level in ["Low", "Moderate", "High"]:
        sub = frame[frame["Addiction_Category"] == level]
        if sub.empty:
            continue
        fig.add_bar(
            x=sub[category].astype(str).tolist(),
            y=sub["share"].astype(float).tolist(),
            name=level,
            marker_color=ADDICTION_PALETTE.get(level, PALETTE["primary"]),
            text=[f"{v:.1f}%" for v in sub["share"].astype(float)],
            textposition="inside",
        )
    fig.update_layout(
        barmode="stack",
        title=_title(title),
        yaxis=dict(ticksuffix="%", range=[0, 100]),
    )
    return _flat_layout(fig, height=400, has_legend=True)
