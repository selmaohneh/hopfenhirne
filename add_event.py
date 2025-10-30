#!/usr/bin/env python3
import json
import sys
from pathlib import Path
from datetime import datetime


def main():
    if len(sys.argv) != 4:
        print("Usage: add_event.py <date> <time> <name>")
        sys.exit(1)

    date_str = sys.argv[1]
    time_str = sys.argv[2]
    name = sys.argv[3]

    # Validate date format
    try:
        event_date = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        print(f"Error: Invalid date format '{date_str}'. Expected YYYY-MM-DD")
        sys.exit(1)

    # Validate time format
    try:
        datetime.strptime(time_str, "%H:%M")
    except ValueError:
        print(f"Error: Invalid time format '{time_str}'. Expected HH:MM")
        sys.exit(1)

    # Check if date is in the past
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    if event_date.date() < today.date():
        print(f"Error: Date {date_str} is in the past")
        sys.exit(1)

    # Load existing events or create empty list
    events_file = Path("events.json")
    if events_file.exists():
        with open(events_file, 'r', encoding='utf-8') as f:
            events = json.load(f)
    else:
        events = []

    # Create new event
    new_event = {
        "date": date_str,
        "time": time_str,
        "name": name
    }

    # Check if event already exists (same date, time, and name)
    existing_index = None
    for i, event in enumerate(events):
        if (event.get("date") == date_str and
            event.get("time") == time_str and
            event.get("name") == name):
            existing_index = i
            break

    if existing_index is not None:
        print(f"Event already exists at index {existing_index}")
    else:
        # Add new event
        events.append(new_event)
        print(f"Added new event: {new_event}")

    # Sort events by date and time
    events.sort(key=lambda e: (e.get("date", ""), e.get("time", "")))

    # Write back to file
    with open(events_file, 'w', encoding='utf-8') as f:
        json.dump(events, f, indent=2, ensure_ascii=False)

    print(f"Events file updated successfully")


if __name__ == "__main__":
    main()
