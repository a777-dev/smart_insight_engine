# Region-Aware Behavioral Risk Prediction

A Streamlit application that predicts stress, addiction, and productivity risk from unified smartphone, sleep, and lifestyle data across India, USA, and Global cohorts.

## Project Highlights

- Multi-source behavioral dataset: 16,000 records, 24+ harmonized features
- RandomForest stress (regression), addiction (classification), and productivity (classification) models
- KMeans archetype clustering with five behavioral personas
- Region-aware analytics (India / USA / Global)
- Students vs Professionals segmentation
- Explainable AI: global feature importance + local sensitivity
- Scenario simulation engine with before/after comparison
- Smart insight engine with rule + model-aware recommendations

## Repository Layout

```
region_aware_risk_pred/
  Home.py
  run_streamlit.py
  requirements.txt
  unified_behavioral_intelligence.csv
  data/
    processed_behavioral_data.csv
  models/
    stress_model.pkl
    addiction_model.pkl
    productivity_model.pkl
    preprocessor.pkl
    cluster_bundle.pkl
    model_metadata.json
  pages/
    1_Region_Aware_Analytics.py
    2_Students_vs_Professionals.py
    3_AI_Risk_Prediction.py
    4_Behavioral_Archetypes.py
    5_Explainable_AI.py
    6_Scenario_Simulation.py
    7_Smart_Insight_Engine.py
  scripts/
    train_models.py
  src/
    __init__.py
    analytics.py
    bootstrap.py
    charts.py
    config.py
    data.py
    inference.py
    insights.py
    styles.py
    training.py
  tests/
    test_inference.py
```

## Setup

```powershell
python -m pip install -r requirements.txt
```

## Train Models

```powershell
python scripts\train_models.py
```

This regenerates the model artifacts in `models/` and the processed dataset in `data/`.

## Run The App

```powershell
python run_streamlit.py
```

Then open http://localhost:8501

## Pages

1. **Behavioral Overview** — KPI cards, lifestyle gauges, balance radar
2. **Region-Aware Analytics** — India vs USA vs Global cohort comparison
3. **Students vs Professionals** — split-screen behavioral comparison
4. **AI Risk Prediction** — model metrics and live predictions
5. **Behavioral Archetypes** — KMeans cluster constellation and personas
6. **Explainable AI** — global feature importance + local sensitivity bars
7. **Scenario Simulation** — interactive what-if engine
8. **Smart Insight Engine** — 3 to 5 personalized recommendations

## Run Tests

```powershell
python -m unittest discover -s tests -v
```

## Notes

Outputs are predictive estimates from a unified synthetic-source dataset; intended for behavioral research and exploration, not clinical diagnosis.
