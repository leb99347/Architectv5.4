import argparse
from schema_tools.schema_validator import validate_all_logs
from schema_tools.schema_checker import check_integrity
from schema_tools.schema_repair import repair_logs
from shadow_summary import summarize_shadow_trades
from log_exporter import export_all_to_csv

def main():
    parser = argparse.ArgumentParser(description="Audit Engine CLI")
    parser.add_argument("--validate", action="store_true", help="Validate log files against schema")
    parser.add_argument("--check", action="store_true", help="Check log integrity")
    parser.add_argument("--repair", action="store_true", help="Attempt auto-repair logs")
    parser.add_argument("--summary", action="store_true", help="Summarize shadow vs live trades")
    parser.add_argument("--export", action="store_true", help="Export logs to CSV")

    args = parser.parse_args()

    if args.validate:
        validate_all_logs()
    if args.check:
        check_integrity()
    if args.repair:
        repair_logs()
    if args.summary:
        summarize_shadow_trades()
    if args.export:
        export_all_to_csv()

if __name__ == "__main__":
    main()
