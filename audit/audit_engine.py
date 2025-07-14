"""
audit_engine.py — Reviews trade logs and summarizes outcomes
"""

import json

TRADE_LOG = "logs/trades_executed.jsonl"

def summarize_trades():
    trades = []
    with open(TRADE_LOG, "r") as f:
        for line in f:
            trades.append(json.loads(line))

    print(f"🔎 Total Trades Logged: {len(trades)}")
    for trade in trades[-5:]:
        print(f"- {trade['timestamp']} | {trade['direction']} | {trade['entry_price']} | {trade['mode']}")
