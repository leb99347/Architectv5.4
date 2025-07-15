(.venv) .venvlemicha@Lemichas-MacBook-Pro ArchitectV4_Project_Starter % python3 -c "from indicators.news_filter import should_block_trade; import datetime; import pytz; t = datetime.datetime(2025, 7, 15, 14, 25, tzinfo=pytz.UTC); print(should_block_trade(t))"
True
(.venv) .venvlemicha@Lemichas-MacBook-Pro ArchitectV4_Project_Starter % >....                                                                   
    }

    # Final trading decision
    if bullish_signal:
        action = "buy"
    elif bearish_signal:
        action = "sell"
    else:
        action = "hold"

    return {
        "instrument": "GBP_JPY",
        "action": action,
        "confidence": None,  # populated by confidence model later
        "tier": None,
        "tags": {
            "trend_alignment": signal_dict["trend_alignment"],
            "multi_tap_score": multi_tap_score,
            "atr_ratio": atr_ratio,
            "doji": is_doji(current),
            "ema_filter": bullish_trend or bearish_trend,
            "breakout_strength": signal_dict["breakout_strength"]
        },
        **signal_dict
    )