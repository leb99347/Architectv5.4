
# -------------------------------------------------------
# STEP 5 — Exit Strategy Evaluation (Trailing Stop, Drawdown, Liquidity, News)
# -------------------------------------------------------
try:
    from strategies.exit_strategy import evaluate_exit_conditions

    mock_trade = {
        "entry_price": 187.500,
        "side": "buy",
        "stop_loss": 187.100,
        "atr_multiplier": 1.5,
        "trailing_type": "atr",
        "drawdown_limit": 0.03,
        "sl_buffer": 0.1
    }

    mock_context = {
        "atr": 0.25,
        "volume": 9500,
        "spread": 0.8,
        "time": "2025-07-15T14:29:00Z"
    }

    current_price = 187.620

    print("\n🛑 Testing exit strategy logic:")
    exit_decision = evaluate_exit_conditions(mock_trade, current_price, mock_context)
    print(f"🔎 Exit Decision: {exit_decision}")

except Exception:
    print("❌ Exit strategy logic test failed:")
    traceback.print_exc()

print("-" * 50)

# -------------------------------------------------------
# STEP 5 — Exit Strategy Evaluation (Trailing Stop, Drawdown, Liquidity, News)
# -------------------------------------------------------
try:
    from strategies.exit_strategy import evaluate_exit_conditions

    mock_trade = {
        "entry_price": 187.500,
        "side": "buy",
        "stop_loss": 187.100,
        "atr_multiplier": 1.5,
        "trailing_type": "atr",
        "drawdown_limit": 0.03,
        "sl_buffer": 0.1
    }

    mock_context = {
        "atr": 0.25,
        "volume": 9500,
        "spread": 0.8,
        "time": "2025-07-15T14:29:00Z"
    }

    current_price = 187.620

    print("\n🛑 Testing exit strategy logic:")
    exit_decision = evaluate_exit_conditions(mock_trade, current_price, mock_context)
    print(f"🔎 Exit Decision: {exit_decision}")

except Exception:
    print("❌ Exit strategy logic test failed:")
    traceback.print_exc()

print("-" * 50)

# -------------------------------------------------------
# STEP 5 — Exit Strategy Evaluation (Trailing Stop, Drawdown, Liquidity, News)
# -------------------------------------------------------
try:
    from strategies.exit_strategy import evaluate_exit_conditions

    mock_trade = {
        "entry_price": 187.500,
        "side": "buy",
        "stop_loss": 187.100,
        "atr_multiplier": 1.5,
        "trailing_type": "atr",
        "drawdown_limit": 0.03,
        "sl_buffer": 0.1
    }

    mock_context = {
        "atr": 0.25,
        "volume": 9500,
        "spread": 0.8,
        "time": "2025-07-15T14:29:00Z"
    }

    current_price = 187.620

    print("\n🛑 Testing exit strategy logic:")
    exit_decision = evaluate_exit_conditions(mock_trade, current_price, mock_context)
    print(f"🔎 Exit Decision: {exit_decision}")

except Exception:
    print("❌ Exit strategy logic test failed:")
    traceback.print_exc()

print("-" * 50)

# -------------------------------------------------------
# STEP 5 — Exit Strategy Evaluation (Trailing Stop, Drawdown, Liquidity, News)
# -------------------------------------------------------
try:
    from strategies.exit_strategy import evaluate_exit_conditions

    mock_trade = {
        "entry_price": 187.500,
        "side": "buy",
        "stop_loss": 187.100,
        "atr_multiplier": 1.5,
        "trailing_type": "atr",
        "drawdown_limit": 0.03,
        "sl_buffer": 0.1
    }

    mock_context = {
        "atr": 0.25,
        "volume": 9500,
        "spread": 0.8,
        "time": "2025-07-15T14:29:00Z"
    }

    current_price = 187.620

    print("\n🛑 Testing exit strategy logic:")
    exit_decision = evaluate_exit_conditions(mock_trade, current_price, mock_context)
    print(f"🔎 Exit Decision: {exit_decision}")

except Exception:
    print("❌ Exit strategy logic test failed:")
    traceback.print_exc()

print("-" * 50)

# -------------------------------------------------------
# STEP 5 — Exit Strategy Evaluation (Trailing Stop, Drawdown, Liquidity, News)
# -------------------------------------------------------
try:
    from strategies.exit_strategy import evaluate_exit_conditions

    mock_trade = {
        "entry_price": 187.500,
        "side": "buy",
        "stop_loss": 187.100,
        "atr_multiplier": 1.5,
        "trailing_type": "atr",
        "drawdown_limit": 0.03,
        "sl_buffer": 0.1
    }

    mock_context = {
        "atr": 0.25,
        "volume": 9500,
        "spread": 0.8,
        "time": "2025-07-15T14:29:00Z"
    }

    current_price = 187.620

    print("\n🛑 Testing exit strategy logic:")
    exit_decision = evaluate_exit_conditions(mock_trade, current_price, mock_context)
    print(f"🔎 Exit Decision: {exit_decision}")

except Exception:
    print("❌ Exit strategy logic test failed:")
    traceback.print_exc()

print("-" * 50)
