ArchitectV4 v5.4 — Modular Intelligent FX Trading System

Institutional-grade autonomous FX trading system with live + shadow logic, intelligent feedback cycles, A/B variant testing, and AI–human collaboration. Built by Lemicha Bracey to adapt, evolve, and dominate.

---

VISION

ArchitectV4 v5.4 is a modular, Python-based algorithmic trading system designed for maximum profitability, minimal risk, and scalable intelligence. It simulates institutional strategy logic, integrates real-time A/B variant testing, logs every action with version tags, and feeds results into confidence scoring engines and ML feedback modules.

This system is adaptive by design, with an AI-human feedback loop at its core. Nothing trades without traceable logic. Nothing evolves without validation.

---

KEY PRINCIPLES

Modularity: Each component (logging, signal generation, audit, ML, execution) is isolated and swappable

Feedback-Driven: All signals and decisions feed back into confidence modules and Mansa’s feedback engine

Shadow Logic: Live signals are mirrored with A/B strategy variants in a “ghost” test environment

Versioned Logging: Every signal and trade is tagged with a strategy version and logged to JSONL

Human-in-the-Loop: ML does not auto-evolve strategies without human confirmation

Future-Proof: Designed for live trading + ML evolution with full audit transparency and explainability

Visualization-Ready: Outputs can be rendered in UI for backtest diffs, strategy tracking, and export

---

PROJECT STRUCTURE

ArchitectV4_Project_Starter/
├── app.py                  - System entry point
├── .env                    - OANDA API credentials (local)
├── requirements.txt        - Dependencies

├── config/
│   └── settings.py         - Global paths, API config, environment management

├── core/
│   ├── logging.py          - Auto logger for signals, trades, diagnostics
│   └── version_injector.py - Injects v5.4 version into logs

├── data/
│   └── fetch_oanda.py      - OANDA price fetcher using oandapyV20

├── signals/
│   └── signal_generator.py - Main breakout/trend-based signal generator (zone + confirmation logic)

├── execution/
│   └── trade_executor.py   - Live trade executor using OANDA REST (to be activated)

├── audit/
│   ├── export_csv.py       - Export logs to CSV for visualization/UI/analysis
│   ├── shadow_logger.py    - Logs A/B variant strategies for review
│   └── shadow_summary.py   - Summarizes performance of shadow vs. live logic

├── ml/
│   ├── confidence_model.py - Classifies trade signals by risk tier, trend alignment, quality
│   └── mansa_feedback.py   - Feedback engine to evaluate and refine strategy layers

├── logs/
│   ├── trades_log_v5.4.jsonl   - Executed trades (auto-generated)
│   ├── signal_generator_signal.jsonl
│   └── shadow_log.jsonl       - Shadow test log of all A/B strategy outputs

└── test_env.py             - Diagnostic script to test .env + dependencies

---

SIGNAL FLOW

[Market Data Fetch] → [Signal Generator] → [A/B Shadow Logger] → [Live Trade (if valid)] → [Trade Logger] → [Audit + Mansa Feedback]

Every step generates logs → feeds confidence layers → passes to Mansa → returned for UI approval.

---

MANSA INTEGRATION

Mansa is the ML/AI strategic brain of Architect. It reviews:

- Shadow logs
- Signal metadata
- Trade outcomes
- Strategy variants and deltas

Mansa does not override live strategy without approval. It can propose upgrades, classify patterns, and recommend improvements via:

- confidence_model.py
- mansa_feedback.py
- UI visualization layer (coming)

---

STRATEGY CORE

Asset: GBP/JPY

Timeframe: M30 (Execution), H1 (Trend Filter)

Type: Breakout with Retest + Continuation

Zone Detection: Multi-tap structure + swing logic

Entry Confirmation: Full-bodied breakout + ATR filter

Risk: Tiered by confidence score, not hardcoded lot size

Session: London–New York overlap

---

TESTING & DIAGNOSTICS

To run diagnostics:

python3 test_env.py

To manually test modules:

python3 audit/shadow_summary.py
python3 audit/export_csv.py
python3 ml/mansa_feedback.py

---

GITHUB SETUP (BEST PRACTICES)

- Use feature/ branches for strategy variants
- Tag commits by version (v5.4, v5.5-dev)
- Pull requests for any major logic swap (e.g. new confirmation strategy)
- Commit logs are version-tied for historical auditability

---

NEXT PHASE IDEAS

- Live execution toggles for risk tiers
- Confidence scoring engine refinement
- Real-time UI dashboard (Streamlit or Flask)
- Slack/Discord alerts from trade log triggers
- Reinforcement learning variant testbed

---

BUILT & CURATED BY

Lemicha Bracey  
Strategist | System Architect | Trader  
lmitdesigns.com
