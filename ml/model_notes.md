# 📊 Confidence Model — ML Strategy Notes (v4.1)

## Objective
Learn a mapping between signal features and profitable outcomes to dynamically score new signals in real-time.

## Input Features
- `trend_alignment` (bool → int)
- `breakout_strength` (float)
- `multi_tap_score` (float)
- `atr_ratio` (float, capped at 2.0)

## Target Variable
- Binary: profitable (1) / not profitable (0)
- Derived from real trade logs only

## Model Pipeline
- Trained using `RandomForestClassifier(n_estimators=100, max_depth=5)`
- Trained on: `logs/trade_log.jsonl`
- Saved to: `ml/trained_confidence_model.pkl`
- Live scoring via: `ml/confidence_model_live.py`

## Fallback
If model is missing or error occurs, fallback to `ml/confidence_model.py` rule-based scorer

---

## Risk Controls
- Confidence scores must pass dynamic thresholds (`tier_3`, `tier_2`, etc.)
- Learning strictly from `logs/trade_log.jsonl` and `logs/shadow_log.jsonl`
- No synthetic or hallucinated labels allowed