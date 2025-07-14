"""
shadow_summary.py — Compares shadow strategy variant results
"""

import json
from collections import defaultdict

LOG_FILE = "logs/shadow_log.jsonl"

def summarize_shadows():
    stats = defaultdict(int)
    try:
        with open(LOG_FILE, "r") as f:
            for line in f:
                result = json.loads(line)
                variant = result["variant"]
                stats[variant] += 1
    except FileNotFoundError:
        print("No shadow logs found.")
        return

    print("📊 Shadow Strategy Summary:")
    for variant, count in stats.items():
        print(f" - {variant}: {count} signals evaluated")

if __name__ == "__main__":
    summarize_shadows()
