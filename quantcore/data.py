"""Deterministic artificial observations and strict pipeline validation."""
import csv
import math
from datetime import date
from pathlib import Path

def validate(prices):
    values = tuple(float(x) for x in prices)
    if len(values) < 2 or any(not math.isfinite(x) or x <= 0 for x in values):
        raise ValueError("Need at least two finite positive prices")
    return values

def synthetic_prices(length=96):
    if not isinstance(length, int) or length < 2:
        raise ValueError("length must be at least two")
    return tuple(100 + i * .07 + 3 * math.sin(i * .43) for i in range(length))

def load_csv(path: Path):
    with path.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    dates = [date.fromisoformat(row["date"]) for row in rows]
    if dates != sorted(set(dates)):
        raise ValueError("Dates must be unique and chronological")
    if any(row["symbol"] != "SYNTH" for row in rows):
        raise ValueError("Only the artificial fixture is supported")
    return validate(row["close"] for row in rows)
