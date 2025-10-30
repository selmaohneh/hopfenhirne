#!/usr/bin/env python3
import json
import os
from pathlib import Path
from collections import defaultdict


def main():
    data_dir = Path("data")

    if not data_dir.exists():
        return

    # Initialize statistics dictionary
    stats = defaultdict(lambda: {
        "attendances": 0,
        "quizmaster_count": 0,
        "hopfenhirn_des_monats_count": 0,
        "wins": 0,
        "played_events": 0,
        "winrate": 0.0
    })

    # Process all JSON files in the data directory
    json_files = sorted(data_dir.glob("*.json"))

    if not json_files:
        return

    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                event_data = json.load(f)

            attendees = event_data.get("attendees", [])
            quizmasters = event_data.get("quizmasters", [])
            winners = event_data.get("winners", [])
            has_quiz = len(quizmasters) > 0

            # Count attendances
            for attendee in attendees:
                stats[attendee]["attendances"] += 1

                # Count events where person played (was not quizmaster and there was a quiz)
                if has_quiz and attendee not in quizmasters:
                    stats[attendee]["played_events"] += 1

            # Count quizmasters
            for quizmaster in quizmasters:
                stats[quizmaster]["quizmaster_count"] += 1

            # Count wins (only when there was a quiz, person was attendee, and not quizmaster)
            if has_quiz:
                for winner in winners:
                    if winner in attendees and winner not in quizmasters:
                        stats[winner]["wins"] += 1

            # Count hopfenhirn des monats
            hopfenhirn = event_data.get("hopfenhirn_des_monats")
            if hopfenhirn:
                stats[hopfenhirn]["hopfenhirn_des_monats_count"] += 1

        except Exception as e:
            continue

    # Calculate win rates (only count events where they actually played)
    for person, person_stats in stats.items():
        played_events = person_stats["played_events"]

        if played_events > 0:
            person_stats["winrate"] = round(person_stats["wins"] / played_events, 4)
        else:
            person_stats["winrate"] = 0.0

    # Convert defaultdict to regular dict and sort by attendances (descending)
    stats_dict = dict(stats)
    sorted_stats = dict(sorted(
        stats_dict.items(),
        key=lambda x: (x[1]["attendances"], x[1]["wins"]),
        reverse=True
    ))

    # Write stats to JSON file
    output_file = "stats.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(sorted_stats, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
