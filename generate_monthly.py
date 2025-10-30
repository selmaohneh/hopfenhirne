#!/usr/bin/env python3
import json
from pathlib import Path


def main():
    data_dir = Path("data")

    if not data_dir.exists():
        return

    # Get all JSON files and sort by filename (which are dates YYYY-MM-DD)
    json_files = sorted(data_dir.glob("*.json"))

    if not json_files:
        return

    # Get the latest event file
    latest_file = json_files[-1]

    with open(latest_file, 'r', encoding='utf-8') as f:
        event_data = json.load(f)

    # Extract winners and hopfenhirn des monats
    monthly_data = {
        "date": event_data.get("date"),
        "winners": event_data.get("winners", []),
        "hopfenhirn_des_monats": event_data.get("hopfenhirn_des_monats")
    }

    # Write to monthly.json
    output_file = "monthly.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(monthly_data, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
