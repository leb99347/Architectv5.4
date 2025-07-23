# test_env.py — Diagnostic Tool for ArchitectV4

import os
from dotenv import load_dotenv

def test_env_variables():
    print("\n🔧 Testing Environment Variables:")
    load_dotenv()
    api_key = os.getenv("OANDA_API_KEY")
    account_id = os.getenv("OANDA_ACCOUNT_ID")

    if api_key and account_id:
        print(f"✅ OANDA_API_KEY loaded: {api_key[:6]}... (length: {len(api_key)})")
        print(f"✅ OANDA_ACCOUNT_ID loaded: {account_id}")
    else:
        print("❌ Missing environment variables.")
        if not api_key: print("  - OANDA_API_KEY is missing.")
        if not account_id: print("  - OANDA_ACCOUNT_ID is missing.")

def test_imports():
    print("\n🧪 Testing Core Module Imports:")
    try:
        import oandapyV20
        import pandas
        import numpy
        import sklearn
        print("✅ All core dependencies imported successfully.")
    except ImportError as e:
        print(f"❌ Import failed: {e}")

def test_paths():
    print("\n📁 Checking Project Paths:")
    paths = [
        "config/__init__.py",
        "core/logging.py",
        "data/fetch_oanda.py",
        "signals/signal_generator.py",
        "ml/confidence_model.py",
        "execution/trade_executor.py",
        "audit/audit_engine.py",
        "shadow/shadow_tester.py"
    ]
    for path in paths:
        exists = os.path.exists(path)
        print(f"{'✅' if exists else '❌'} {path}")

if __name__ == "__main__":
    print("🧠 ArchitectV4 System Diagnostic")
    test_env_variables()
    test_imports()
    test_paths()
