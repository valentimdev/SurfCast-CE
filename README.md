# SurfCast CE – Ceará Surf‑Forecast Advisor

#### Video Demo:[Youtube Video](https://www.youtube.com/watch?v=ldTZ7ZQSowg);
#### Description:
**SurfCast CE** is a Python tool that helps surfers in Ceará, Brazil, choose the best beach to surf based on weather data. It gets information about wave height and wind speed from the Stormglass API, then calculates a score for each beach.
####
The program supports four popular beaches: Praia do Futuro, Iguape, Paracuru, and Taíba. It shows the best beach for the day based on wave conditions and wind, and you can also get the data in JSON format for automation.
---

## Overview

**SurfCast CE** is a pure‑Python command‑line utility that helps surfers in Ceará, Brazil, decide **where** to paddle out each day.  The script queries the *Stormglass* marine‑weather API v2 for four popular breaks—Praia do Futuro, Iguape, Paracuru, and Taíba—and converts raw conditions into a single **surf score** (0 – 10).  The beach with the highest score is highlighted in the console, or returned as JSON for automation.

*Built for Harvard CS50P’s final project spec – single‑file app (**`project.py`**), 3 testable helpers, and **`pytest`** coverage.*

---

## Features

- **Live forecast**: wave height & wind speed retrieved hourly via Stormglass v2.
- **Scoring algorithm**: 60 % weight to wave height (1 m ideal), 40 % to wind (≤ 12 kt ideal).
- **Rich output**: colour table + 🏄 icon for the recommended spot.
- `--json` flag for machine‑readable output.
- `.env` support via **python‑dotenv** – keep your API key out of shell history.
- 3 unit tests (`compute_score`, `choose_beach`, `format_report`) to guard logic.

---

## File Layout

| File               | Purpose                                                                                                |
| ------------------ | ------------------------------------------------------------------------------------------------------ |
| `project.py`       | Main program & functions (`main`, `fetch_forecast`, `compute_score`, `choose_beach`, `format_report`). |
| `test_project.py`  | Pytest suite covering the three helper functions.                                                      |
| `requirements.txt` | `requests`, `rich`, `python-dotenv`, `pytest`.                                                         |
| `.env.example`     | Template for your Stormglass API key.                                                                  |

---

## Quick Start

```bash
# 1.  set up virtual env (recommended)
python -m venv venv && source venv/bin/activate  # Windows: venv\Scripts\activate

# 2.  install dependencies
pip install -r requirements.txt

# 3.  add your Stormglass token
cp .env.example .env      # then edit, or:
echo "STORMGLASS_API_KEY=YOUR_TOKEN" > .env

# 4.  run!
python project.py               # today
python project.py -d 2025-07-04 # any date (YYYY‑MM‑DD)
python project.py --json        # raw JSON output

# 5.  run tests
pytest -q                       # should show 3 passed
```

---

## How It Works

1. **Fetch** – `fetch_forecast` converts the requested date into Unix timestamps and calls `/v2/weather/point` with waveHeight & windSpeed params.
2. **Score** – `compute_score` normalises each metric (ideal wave ≈ 1 m; wind ≈ 0 kt) to 0–1, weighs them, and rescales to 0–10.
3. **Rank** – `choose_beach` picks the highest‑scoring beach.
4. **Display** – `format_report` prints a pretty table (or JSON).

---

