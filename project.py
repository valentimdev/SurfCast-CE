
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
from dataclasses import dataclass
from typing import Dict, List, Any

import requests
from rich.console import Console
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://api.stormglass.io/v2/weather/point"
PARAM_LIST = ["waveHeight", "windSpeed"]

console = Console()


@dataclass(frozen=True)
class Beach:
    name: str
    lat: float
    lon: float


BEACHES: List[Beach] = [
    Beach("Praia do Futuro", -3.7208, -38.4807),
    Beach("Iguape", -4.0791, -38.4503),
    Beach("Paracuru", -3.4146, -39.0300),
    Beach("Taíba", -3.5480, -38.8929),
]


def _unix(ts: dt.datetime) -> int:
    return int(ts.replace(tzinfo=dt.timezone.utc).timestamp())


def fetch_forecast(beach: Beach, date: dt.date) -> Dict[str, Any]:
    token = os.environ.get("STORMGLASS_API_KEY")
    if not token:
        raise RuntimeError("Set STORMGLASS_API_KEY in a .env file or environment variable.")

    start = _unix(dt.datetime.combine(date, dt.time.min))
    end = _unix(dt.datetime.combine(date + dt.timedelta(days=1), dt.time.min))

    params = {
        "lat": beach.lat,
        "lng": beach.lon,
        "params": ",".join(PARAM_LIST),
        "start": start,
        "end": end,
    }

    headers = {"Authorization": token}
    resp = requests.get(API_URL, params=params, headers=headers, timeout=15)
    resp.raise_for_status()
    return resp.json()


def compute_score(forecast: Dict[str, Any]) -> float:

    hours = forecast.get("hours", [])
    waves = [h["waveHeight"]["noaa"] for h in hours if "waveHeight" in h]
    winds = [h["windSpeed"]["noaa"] for h in hours if "windSpeed" in h]

    if not waves or not winds:
        return 0.0


    wave_score = sum(max(0, 1 - abs(h - 1)) for h in waves) / len(waves)
    wind_score = sum(max(0, 1 - s / 12) for s in winds) / len(winds)

    return round((0.6 * wave_score + 0.4 * wind_score) * 10, 2)


def choose_beach(scores: Dict[str, float]) -> str:
    if not scores:
        raise ValueError("scores dict is empty")
    return max(scores.items(), key=lambda kv: kv[1])[0]


def format_report(scores: Dict[str, float], best: str, date: dt.date) -> str:
    lines = [f"SurfCast CE for {date:%d %b %Y}", "-" * 34]
    for beach, score in sorted(scores.items(), key=lambda kv: kv[1], reverse=True):
        prefix = "🏄 " if beach == best else "   "
        lines.append(f"{prefix}{beach:<18}{score:>5.1f}")
    lines.append(f"\nRecommendation: {best}")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="SurfCast CE – choose your beach.")
    parser.add_argument("-d", "--date", type=lambda s: dt.datetime.strptime(s, "%Y-%m-%d").date(), default=dt.date.today())
    parser.add_argument("--json", action="store_true", help="Raw JSON output")
    args = parser.parse_args()

    scores: Dict[str, float] = {}
    for beach in BEACHES:
        try:
            data = fetch_forecast(beach, args.date)
            scores[beach.name] = compute_score(data)
        except Exception as e:
            console.print(f"[red]Error fetching {beach.name}: {e}[/red]")

    if not scores:
        console.print("[red]Failed to retrieve any forecasts.[/red]")
        sys.exit(1)

    best = choose_beach(scores)

    if args.json:
        print(json.dumps({"date": args.date.isoformat(), "scores": scores, "best": best}))
    else:
        console.print(format_report(scores, best, args.date))


if __name__ == "__main__":
    main()
