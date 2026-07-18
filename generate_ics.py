#!/usr/bin/env python3
import json
from pathlib import Path

CALENDAR_NAME = "Hopfenhirne Stammtisch"
DOMAIN = "hopfenhirne.de"
WEBSITE_URL = "https://www.hopfenhirne.de"
# Default event duration; events.json has no end time
EVENT_DURATION = "PT4H"

VTIMEZONE = """BEGIN:VTIMEZONE
TZID:Europe/Berlin
BEGIN:DAYLIGHT
TZOFFSETFROM:+0100
TZOFFSETTO:+0200
TZNAME:CEST
DTSTART:19700329T020000
RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=-1SU
END:DAYLIGHT
BEGIN:STANDARD
TZOFFSETFROM:+0200
TZOFFSETTO:+0100
TZNAME:CET
DTSTART:19701025T030000
RRULE:FREQ=YEARLY;BYMONTH=10;BYDAY=-1SU
END:STANDARD
END:VTIMEZONE"""


def escape_text(value):
    """Escape text for iCalendar TEXT values (RFC 5545 3.3.11)."""
    return (
        value.replace("\\", "\\\\")
        .replace(";", "\\;")
        .replace(",", "\\,")
        .replace("\n", "\\n")
    )


def fold_line(line):
    """Fold content lines longer than 75 octets (RFC 5545 3.1)."""
    encoded = line.encode("utf-8")
    if len(encoded) <= 75:
        return line
    parts = []
    limit = 75
    while encoded:
        cut = min(limit, len(encoded))
        # Don't split inside a multi-byte UTF-8 sequence: back up while the
        # byte at the cut position is a UTF-8 continuation byte (0b10xxxxxx)
        while cut < len(encoded) and (encoded[cut] & 0xC0) == 0x80:
            cut -= 1
        parts.append(encoded[:cut].decode("utf-8"))
        encoded = encoded[cut:]
        limit = 74  # continuation lines start with a space
    return "\n ".join(parts)


def build_vevent(event):
    date = event["date"]
    time = event.get("time", "19:00")
    name = event.get("name", "Stammtisch")

    date_compact = date.replace("-", "")
    time_compact = time.replace(":", "") + "00"

    # Deterministic DTSTAMP derived from the event data so the output only
    # changes when events.json changes
    dtstamp = f"{date_compact}T{time_compact}Z"

    return "\n".join(
        [
            "BEGIN:VEVENT",
            f"UID:{date_compact}@{DOMAIN}",
            f"DTSTAMP:{dtstamp}",
            f"DTSTART;TZID=Europe/Berlin:{date_compact}T{time_compact}",
            f"DURATION:{EVENT_DURATION}",
            fold_line(f"SUMMARY:{escape_text(name)}"),
            fold_line(f"DESCRIPTION:{escape_text(f'Quiz-Stammtisch der Hopfenhirne. Alle Infos: {WEBSITE_URL}')}"),
            f"URL:{WEBSITE_URL}",
            "END:VEVENT",
        ]
    )


def main():
    events_file = Path("events.json")
    if events_file.exists():
        with open(events_file, "r", encoding="utf-8") as f:
            events = json.load(f)
    else:
        events = []

    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        f"PRODID:-//Hopfenhirne//Stammtisch Kalender//DE",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        f"X-WR-CALNAME:{CALENDAR_NAME}",
        "X-WR-TIMEZONE:Europe/Berlin",
        # Hint for clients how often to refresh the subscription
        "REFRESH-INTERVAL;VALUE=DURATION:PT12H",
        "X-PUBLISHED-TTL:PT12H",
        VTIMEZONE,
    ]

    for event in sorted(events, key=lambda e: (e.get("date", ""), e.get("time", ""))):
        lines.append(build_vevent(event))

    lines.append("END:VCALENDAR")

    # RFC 5545 requires CRLF line endings
    content = "\n".join(lines).replace("\n", "\r\n") + "\r\n"

    with open("events.ics", "w", encoding="utf-8", newline="") as f:
        f.write(content)

    print(f"Generated events.ics with {len(events)} event(s)")


if __name__ == "__main__":
    main()
