# scripts/fetch_oanda_candles.py

import os
import oandapyV20
import pandas as pd
from datetime import datetime
from oandapyV20.endpoints.instruments import InstrumentsCandles

def fetch_ohlcv_data(
    instrument="GBP_JPY",
    granularity="M30",
    count=500,
    price="M",  # Midpoint candles
    output_csv="data/sample_gbpjpy_ohlcv.csv"
):
    client = oandapyV20.API(access_token=os.getenv("OANDA_API_KEY"))

    params = {
        "granularity": granularity,
        "count": count,
        "price": price
    }

    r = InstrumentsCandles(instrument=instrument, params=params)
    client.request(r)

    candles = r.response.get("candles", [])
    records = []

    for c in candles:
        if not c["complete"]:
            continue  # skip incomplete candles

        record = {
            "timestamp": c["time"],
            "open": float(c["mid"]["o"]),
            "high": float(c["mid"]["h"]),
            "low": float(c["mid"]["l"]),
            "close": float(c["mid"]["c"]),
            "volume": c["volume"]
        }
        records.append(record)

    df = pd.DataFrame(records)
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    df.to_csv(output_csv, index=False)

    print(f"✅ Saved {len(df)} candles to {output_csv}")
    print(df.tail())

if __name__ == "__main__":
    fetch_ohlcv_data()