 # ArchitectV4 Confidence Model Upgrade Plan

## 🧠 Vision: Self-Learning, Precision-Scoring System

Design a robust, intelligent signal scoring system that:

* **Learns autonomously from real trade outcomes** — no hallucinated data
* **Assigns precision-based confidence tiers** for risk-managed execution
* **Feeds into a real-time feedback loop (Mansa) for AI-human co-evolution**
* **Optimizes compounding dynamically** with elite-level calibration

---

## 🌐 Current System (v4.0 - v5.3) Snapshot

### Current Mechanics:

* Signal scoring relies on hardcoded weights for indicators:

  * Doji candle presence
  * EMA trend alignment
  * Session filter (London/NY)
  * Pivot zone strength
  * ATR volatility filter
* Signals are passed if they meet a static threshold (e.g. 0.7)

### Gaps Identified:

| Flaw                       | Risk to System                              | Fix Needed                              |
| -------------------------- | ------------------------------------------- | --------------------------------------- |
| Static logic               | Fails in shifting market conditions         | Dynamic model from live data            |
| No learning                | Cannot adapt or evolve                      | ML-driven feedback model                |
| Binary signal cutoff       | No gradation of confidence                  | Tiered scoring + staging                |
| Tag synergy ignored        | Loses info on which combos work best        | Feature interaction tracking            |
| Manual optimization        | Human bias & rigidity                       | Self-adjusting weights + explainability |
| No maintenance interface   | Blind spots from version drift              | Continuous audit pipeline               |
| Weak integration with logs | Model not fed from same source as execution | Unified data tap                        |

---

## 📊 Phase 1: Trade & Shadow Logging Infrastructure

### Logging Enhancements:

* [x] `trade_logger.py` captures:

  * Confidence score (0.0–1.0)
  * Active indicator tags (e.g. ema\_filter=True, doji=True)
  * Market session, volatility regime, S/R zone type
  * Trade outcome: win/loss, net pips, duration
  * Tier (0–3)
* [x] Shadow logs mirror real logs identically
* [x] Stored in `logs/trade_log.jsonl` and `logs/shadow_log.jsonl`
* [x] Auto-tagged with strategy version

This forms the **true historical dataset** for ML training and feedback analysis.

---

## 🧠 Phase 2: Sklearn-Based Trainable Confidence Model

### Feature Inputs:

* Binary indicators (doji, ema, atr\_filter, session)
* Breakout candle strength (relative to ATR)
* Volatility score (normalized)
* Zone tap count (multi-tap validation)
* Market session (London, NY)
* Recent market regime (low/high volatility)
* Strategy version tag

### Target:

* Binary classification: **profitable (1) / not profitable (0)**
* Optional: bucketing into strong win / minor win / break-even / loss

### Models to Evaluate:

* RandomForestClassifier ✅
* XGBoost ✅
* LogisticRegression (baseline)
* LightGBM (for future speed optimizations)

### Output:

* `confidence_score ∈ [0.0, 1.0]`
* Predicted tier
* Per-tag and tag-combo attribution

---

## 🤖 Phase 3: Mansa AI-Human Feedback Loop

### Module: `ml/mansa_feedback.py`

* Reads from trade + shadow logs
* Compares actual vs predicted outcomes by tag combinations
* Flags underperformers (e.g., "high confidence + session=NY + doji only = net loss")
* Generates:

  * Suggested tag adjustments
  * Confidence threshold updates
  * Feature impact visualizations
* Saves to `mansa_suggestions.json`
* Routes outputs to:

  * Frontend diagnostics
  * Model retraining triggers
  * Strategist prompt queue

### Frontend Integration:

* Confidence distribution visualizer
* Tiered win rate graphs
* Combination heatmaps (win rate by feature combo)
* Human override input (approve/reject Mansa proposals)
* Alert flags for version drift or tag decay

---

## 🎯 Phase 4: Tiered Execution Framework

```python
CONFIDENCE_THRESHOLDS = {
  "tier_3": 0.85,  # Full-size, live
  "tier_2": 0.70,  # Partial-size, live
  "tier_1": 0.55,  # Shadow trade only
  "tier_0": 0.00   # Ignore
}
```

Execution module reads tier and routes trade accordingly.
Tagged version flows into shadow/live and logs.

---

## 🧬 Phase 5: Precision Compounding Engine

* Tier determines **risk size multiplier** (e.g., 1.0x, 0.5x, 0.2x)
* Daily equity curve influences adaptive risk scaling
* Guardrails:

  * Daily drawdown lock
  * Cooldown after high-volatility loss
  * Limit resets after recovery
* Compounding respects confidence tier slope across the week
* Optionally throttle trade count by volatility or news proximity

---

## 🧠 Phase 6: Real-Data-Only Learning Discipline

* Model **only trains on validated backtest/live logs**
* No synthetic augmentation or simulated data
* Shadow logs form a sandboxed learning set
* All outcomes are versioned, and models are tagged with compatible bot version
* Manual override requires rationale and rollback ability

---

## 🔧 Phase 7: Analysis + Maintenance Layer

* `audit/shadow_summary.py`: Summarize shadow trade outcomes by tag/tier/version
* `audit/export_csv.py`: Converts `.jsonl` logs into tabular CSV for ML use
* `core/logging.py`: Unified logger routes shadow/live data uniformly
* `ml/confidence_model.py`: Retrains model from latest logs
* `ml/mansa_feedback.py`: Feedback brain suggesting logic edits and retrains
* Frontend: Visual diagnostics, toggle switch for audit view, approval UI

---

## 🌌 Final System Architecture

```
+----------------------------+
|      Signal Generator      |
+-------------+--------------+
              |
      +-------v--------+
      | Confidence Model |
      +-------+--------+
              |
    +---------+----------+
    |                    |
+---v---+          +-----v------+
| Shadow |          |   Live     |
| Trades |          | Execution |
+---+---+          +-----+------+
    |                    |
+---v----------+  +------v-------+
| Shadow Logger |  | Trade Logger |
+---------------+  +--------------+
         \              /
          +-----------+
          |   Mansa   |
          +-----------+
              |
     +--------v---------+
     | Human Oversight  |
     +------------------+
```

