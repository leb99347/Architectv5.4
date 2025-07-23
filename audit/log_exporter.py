import pandas as pd
import json, glob

def export_all_to_csv(log_path='logs/*.jsonl', export_path='logs/exported_logs.csv'):
    all_logs = []
    for file in glob.glob(log_path):
        with open(file, 'r') as f:
            all_logs.extend(json.loads(line) for line in f)
    df = pd.DataFrame(all_logs)
    df.to_csv(export_path, index=False)
    print(f"Logs exported successfully to {export_path}")
