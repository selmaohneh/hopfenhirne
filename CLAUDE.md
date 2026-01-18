# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Hopfenhirne is a static website for a German quiz/social group ("Stammtisch"). It tracks events, quiz results, and member statistics. The site is hosted on GitHub Pages at www.hopfenhirne.de.

## Architecture

The project consists of:

- **index.html**: Single-page static website that fetches and displays data from JSON files
- **Python scripts**: Data management utilities run via GitHub Actions
- **data/**: Historical event data files named by date (YYYY-MM-DD.json)
- **JSON files**: `events.json` (upcoming events), `stats.json` (member statistics), `monthly.json` (current month highlights)

### Data Flow

1. Event data is added via GitHub Actions workflow (`add-quiz-data.yml`)
2. `generate_stats.py` aggregates all `data/*.json` files into `stats.json`
3. `generate_monthly.py` extracts the latest event's winners into `monthly.json`
4. `remove_past_events.py` cleans up past events from `events.json` (runs on schedule)

### Event Data Schema (data/YYYY-MM-DD.json)

```json
{
  "date": "YYYY-MM-DD",
  "attendees": ["Name1", "Name2"],
  "quizmasters": ["Name"],
  "winners": ["1st", "2nd", "3rd"],
  "hopfenhirn_des_monats": "Name"
}
```

## Commands

```bash
# Add a new upcoming event
python add_event.py YYYY-MM-DD HH:MM "Event Name"

# Regenerate statistics from all data files
python generate_stats.py

# Update monthly.json from latest event
python generate_monthly.py

# Remove past events from events.json
python remove_past_events.py
```

## GitHub Actions Workflows

- **add-event.yml**: Manual trigger to add upcoming events (creates PR)
- **add-quiz-data.yml**: Manual trigger to add event data with attendees, winners, etc. (creates PR)
- **cleanup-past-events.yml**: Scheduled (every 12h) cleanup of past events from events.json

## Statistics Logic

- `winrate` = wins / played_events (events where person attended but was not quizmaster)
- Website displays only members with `played_events >= 3` in the stats table
- Stats table is sortable by clicking column headers
