#!/usr/bin/env python3
import json
import sys
from pathlib import Path
from datetime import datetime


def main():
    # Load existing events
    events_file = Path("events.json")
    if not events_file.exists():
        print("events.json not found")
        sys.exit(0)

    with open(events_file, 'r', encoding='utf-8') as f:
        events = json.load(f)

    # Get today's date at midnight
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).date()

    # Optional argument: date of an event that already took place (e.g. when
    # its results are entered on the same day). Events up to and including
    # that date are removed as well.
    cutoff = None
    if len(sys.argv) > 1:
        try:
            cutoff = datetime.strptime(sys.argv[1], "%Y-%m-%d").date()
        except ValueError:
            print(f"Invalid date format: {sys.argv[1]} (expected YYYY-MM-DD)")
            sys.exit(1)

    # Filter out past events
    future_events = []
    removed_events = []

    for event in events:
        try:
            event_date = datetime.strptime(event.get("date", ""), "%Y-%m-%d").date()
            if event_date >= today and (cutoff is None or event_date > cutoff):
                future_events.append(event)
            else:
                removed_events.append(event)
        except ValueError:
            # If date parsing fails, keep the event
            print(f"Warning: Could not parse date for event: {event}")
            future_events.append(event)

    # Check if any events were removed
    if not removed_events:
        print("No past events found")
        sys.exit(0)

    # Print removed events
    print(f"Removing {len(removed_events)} past event(s):")
    for event in removed_events:
        print(f"  - {event.get('name')} on {event.get('date')} at {event.get('time')}")

    # Write back to file
    with open(events_file, 'w', encoding='utf-8') as f:
        json.dump(future_events, f, indent=2, ensure_ascii=False)

    # Add newline at end of file
    with open(events_file, 'a', encoding='utf-8') as f:
        f.write('\n')

    print(f"Events file updated successfully")
    sys.exit(0)


if __name__ == "__main__":
    main()
