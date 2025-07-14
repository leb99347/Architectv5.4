"""
export_csv.py — Exports logs as CSV for external analysis or ML training
"""

import json
import csv

def export_shadow_to_csv(jsonl_path="logs/shadow_log.jsonl", output_path="logs/shadow_log.csv"):
    with open(jsonl_path, "r") as infile, open(output_path, "w", newline="") as outfile:
        writer = None
        for line in infile:
            entry = json.loads(line)
            if writer is None:
                writer = csv.DictWriter(outfile, fieldnames=entry.keys())
                writer.writeheader()
            writer.writerow(entry)
    print(f"✅ Shadow log exported to {output_path}")

if __name__ == "__main__":
    export_shadow_to_csv()
