from __future__ import annotations

import streamlit as st


GLOBAL_CSS = """
<style>
  @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&display=swap');

  :root {
    --bg: #FFFFFF;
    --fg: #111827;
    --muted-fg: #4B5563;
    --soft-fg: #6B7280;
    --primary: #3B82F6;
    --primary-strong: #2563EB;
    --secondary: #10B981;
    --accent: #F59E0B;
    --danger: #EF4444;
    --border: #E5E7EB;
    --surface: #F9FAFB;
    --muted: #F3F4F6;
  }

  html, body, [class*="css"] {
    font-family: 'Outfit', ui-sans-serif, system-ui, sans-serif !important;
    color: var(--fg);
  }
  .stApp { background: var(--bg); }

  /* Container */
  .main .block-container {
    max-width: 1280px;
    padding-top: 1.2rem;
    padding-bottom: 4rem;
    padding-left: clamp(0.85rem, 2.4vw, 2rem);
    padding-right: clamp(0.85rem, 2.4vw, 2rem);
  }

  /* Typography */
  h1, h2, h3, h4 {
    font-family: 'Outfit', sans-serif !important;
    color: var(--fg);
    letter-spacing: -0.02em;
    line-height: 1.1;
  }
  h1 { font-size: clamp(1.7rem, 4vw, 2.6rem); margin: 0.2rem 0 0.6rem 0; font-weight: 800; }
  h2 { font-size: clamp(1.25rem, 2.6vw, 1.7rem); margin-top: 1.4rem; font-weight: 700; }
  h3 { font-size: clamp(1.05rem, 2vw, 1.25rem); font-weight: 700; }

  /* Hero */
  .hero-block {
    border: 1px solid var(--border);
    border-left: 6px solid var(--primary);
    padding: clamp(1rem, 2.4vw, 1.6rem) clamp(1rem, 2.4vw, 1.8rem);
    margin-bottom: 1.2rem;
    background: var(--bg);
  }
  .hero-block .eyebrow {
    text-transform: uppercase;
    letter-spacing: 0.18em;
    font-size: 0.72rem;
    font-weight: 700;
    color: var(--primary);
    margin-bottom: 0.4rem;
  }
  .hero-block h1 {
    font-size: clamp(1.7rem, 4.4vw, 2.6rem);
    line-height: 1.05;
    margin: 0 0 0.6rem 0;
  }
  .hero-block p {
    margin: 0;
    color: var(--muted-fg);
    font-size: clamp(0.95rem, 1.6vw, 1.04rem);
    line-height: 1.55;
  }

  /* Metric Cards */
  .metric-card {
    border: 1px solid var(--border);
    padding: 1rem 1.1rem;
    margin-bottom: 0.9rem;
    background: var(--bg);
    min-height: 132px;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
  .metric-card.accent-primary   { border-top: 4px solid var(--primary); }
  .metric-card.accent-secondary { border-top: 4px solid var(--secondary); }
  .metric-card.accent-warning   { border-top: 4px solid var(--accent); }
  .metric-card.accent-accent    { border-top: 4px solid var(--accent); }
  .metric-card.accent-danger    { border-top: 4px solid var(--danger); }
  .metric-card .label {
    text-transform: uppercase;
    letter-spacing: 0.14em;
    font-size: 0.7rem;
    color: var(--soft-fg);
    font-weight: 600;
  }
  .metric-card .value {
    font-size: clamp(1.7rem, 3.2vw, 2.4rem);
    font-weight: 800;
    line-height: 1.1;
    margin: 0.3rem 0;
    color: var(--fg);
    word-break: break-word;
  }
  .metric-card .delta {
    font-size: 0.85rem;
    color: var(--muted-fg);
    margin: 0;
  }

  /* Insight chips */
  .insight-chip {
    border: 1px solid var(--border);
    border-left: 4px solid var(--secondary);
    padding: 0.85rem 1rem;
    margin-bottom: 0.6rem;
    background: var(--surface);
    color: var(--fg);
    line-height: 1.5;
    font-size: 0.95rem;
  }
  .insight-chip.warning { border-left-color: var(--accent); }
  .insight-chip.danger  { border-left-color: var(--danger); }
  .insight-chip strong { color: var(--fg); }

  /* Archetype */
  .archetype-card {
    border: 1px solid var(--border);
    padding: 1rem 1.2rem;
    background: var(--bg);
    margin-bottom: 0.8rem;
    display: flex;
    align-items: flex-start;
    gap: 0.8rem;
    flex-wrap: wrap;
  }
  .archetype-card .icon {
    flex: 0 0 38px;
    width: 38px;
    height: 38px;
    line-height: 38px;
    text-align: center;
    background: var(--primary);
    color: var(--bg);
    font-weight: 800;
    font-size: 0.85rem;
  }
  .archetype-card .body { flex: 1; min-width: 0; }
  .archetype-card h4 { margin: 0; font-size: 1.05rem; font-weight: 700; }
  .archetype-card p { margin: 0.35rem 0 0 0; color: var(--muted-fg); line-height: 1.5; font-size: 0.92rem; }

  /* Section labels */
  .section-title {
    text-transform: uppercase;
    letter-spacing: 0.18em;
    color: var(--soft-fg);
    font-size: 0.76rem;
    font-weight: 700;
    margin-top: 0.6rem;
    margin-bottom: 0.4rem;
  }

  /* Pills */
  .pill {
    display: inline-block;
    padding: 0.25rem 0.6rem;
    background: var(--muted);
    color: var(--fg);
    text-transform: uppercase;
    letter-spacing: 0.12em;
    font-size: 0.68rem;
    font-weight: 700;
    margin: 0 0.4rem 0.4rem 0;
    white-space: nowrap;
  }
  .pill.primary   { background: var(--primary);   color: #FFFFFF; }
  .pill.secondary { background: var(--secondary); color: #FFFFFF; }
  .pill.accent    { background: var(--accent);    color: #FFFFFF; }
  .pill.danger    { background: var(--danger);    color: #FFFFFF; }

  /* Buttons */
  .stButton > button {
    background: var(--primary);
    color: #FFFFFF;
    border: none;
    border-radius: 0;
    padding: 0.75rem 1.2rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    transition: transform 120ms ease, background 120ms ease;
    width: 100%;
  }
  .stButton > button:hover {
    background: var(--primary-strong);
    transform: scale(1.01);
  }
  .stButton > button:focus { outline: 3px solid #BFDBFE; outline-offset: 1px; }

  /* Built-in metric tweak */
  div[data-testid="stMetric"] {
    border: 1px solid var(--border);
    padding: 0.7rem 0.9rem;
    background: var(--bg);
  }

  /* Footer note */
  .footer-note {
    margin-top: 1.6rem;
    border: 1px solid var(--border);
    padding: 1rem 1.1rem;
    color: var(--muted-fg);
    font-size: 0.9rem;
    line-height: 1.5;
    background: var(--surface);
  }

  /* Inputs */
  div[data-baseweb="select"] > div,
  .stTextInput input,
  .stNumberInput input {
    border-radius: 0 !important;
  }

  /* Sliders: keep them readable on dense layouts */
  div[data-testid="stSlider"] label { font-weight: 600; color: var(--fg); font-size: 0.92rem; }

  /* Sidebar - white background, accent navigation */
  section[data-testid="stSidebar"] {
    background: var(--bg) !important;
    border-right: 1px solid var(--border);
  }
  section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a,
  section[data-testid="stSidebar"] [data-testid="stSidebarNav"] span {
    font-weight: 600;
    color: var(--fg);
  }
  section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a:hover {
    background: var(--muted);
  }

  /* Desktop only: lock sidebar open, hide collapse controls */
  @media (min-width: 769px) {
    section[data-testid="stSidebar"] {
      min-width: 260px !important;
      width: 260px !important;
      transform: translateX(0) !important;
      visibility: visible !important;
    }
    button[data-testid="stSidebarCollapseButton"],
    button[data-testid="stSidebarCollapsedControl"],
    button[data-testid="collapsedControl"],
    [data-testid="stSidebarCollapseButton"],
    [data-testid="stSidebarCollapsedControl"],
    [data-testid="collapsedControl"] {
      display: none !important;
      visibility: hidden !important;
    }
  }

  /* Plotly responsiveness */
  div[data-testid="stPlotlyChart"] { width: 100% !important; }
  div[data-testid="stPlotlyChart"] > div { width: 100% !important; }

  /* Tighter spacing on narrow screens */
  @media (max-width: 768px) {
    .main .block-container {
      padding-top: 0.6rem;
      padding-bottom: 2.2rem;
    }
    .hero-block {
      border-left-width: 4px;
      padding: 0.95rem 1rem;
    }
    .hero-block h1 { font-size: 1.7rem; }
    .hero-block p  { font-size: 0.95rem; }
    .metric-card {
      padding: 0.85rem 0.95rem;
      min-height: 108px;
      margin-bottom: 0.7rem;
    }
    .metric-card .value { font-size: 1.55rem; margin: 0.2rem 0; }
    .metric-card .delta { font-size: 0.8rem; }
    .insight-chip { font-size: 0.9rem; padding: 0.75rem 0.9rem; }
    .archetype-card { padding: 0.85rem 0.95rem; }
    .archetype-card h4 { font-size: 1rem; }
    .archetype-card p  { font-size: 0.88rem; }
    .pill { font-size: 0.62rem; padding: 0.2rem 0.5rem; }
    .footer-note { padding: 0.85rem 0.95rem; font-size: 0.85rem; }
    /* Force columns to stack on phones */
    div[data-testid="stHorizontalBlock"] {
      flex-direction: column !important;
      gap: 0.25rem !important;
    }
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
      width: 100% !important;
      flex: 1 1 100% !important;
      min-width: 0 !important;
    }
  }

  /* Tablet: keep 2-up layout for cards */
  @media (min-width: 769px) and (max-width: 1024px) {
    .hero-block h1 { font-size: 2.1rem; }
    .metric-card { min-height: 122px; }
  }
</style>
"""


def apply_styles() -> None:
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


def metric_card(label: str, value: str, delta: str | None = None, accent: str = "primary") -> str:
    delta_html = f'<p class="delta">{delta}</p>' if delta else ""
    return f"""
    <div class="metric-card accent-{accent}">
      <div class="label">{label}</div>
      <div class="value">{value}</div>
      {delta_html}
    </div>
    """


def hero(eyebrow: str, title: str, body: str) -> str:
    return f"""
    <div class="hero-block">
      <div class="eyebrow">{eyebrow}</div>
      <h1>{title}</h1>
      <p>{body}</p>
    </div>
    """


def insight_chip(text: str, tone: str = "default") -> str:
    classes = "insight-chip"
    if tone in {"warning", "danger"}:
        classes += f" {tone}"
    return f'<div class="{classes}">{text}</div>'


def archetype_card(icon: str, title: str, body: str) -> str:
    return f"""
    <div class="archetype-card">
      <div class="icon">{icon}</div>
      <div class="body">
        <h4>{title}</h4>
        <p>{body}</p>
      </div>
    </div>
    """
