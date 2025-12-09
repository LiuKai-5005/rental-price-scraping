# save this as app.py
import csv
import os
from datetime import date, timedelta, datetime
from typing import List

# Add tqdm for progress bar
try:
    from tqdm import tqdm
except ImportError:
    tqdm = None

from plotting import plot_unit_prices
from radius_client import fetch_housing


## check how many day you are interested
NUM_DAYS = 61  # how many days ahead to query
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "Radius")
OUTPUT_PREFIX = os.path.join(OUTPUT_DIR, "house_price")

def collect_unit_rows(check_start_date: date, num_days: int) -> List[List]:
    """
    Query availability for each day in range and collect unit-level rows.
    """
    unit_rows: List[List] = []
    # Track the lowest rent we have seen for each unique plan/floorplan/date/unit combo.
    seen_prices: dict[tuple[str, int, str, str], float] = {}
    progress_iter = tqdm(range(0, num_days + 1), desc="Querying", unit="day") if tqdm else range(0, num_days + 1)

    for i in progress_iter:
        start_date = check_start_date + timedelta(days=i)
        end_date = start_date + timedelta(days=14)
        _, day_mapping = fetch_housing(start_date, end_date)
        for plan, entries in day_mapping.items():
            for floorplan_id, availability_date, unit_name, rent in entries:
                avail_str = availability_date.date().isoformat() if availability_date else ""
                key = (plan, floorplan_id, avail_str, unit_name)
                if key in seen_prices and seen_prices[key] <= rent:
                    # keep the lowest price to avoid duplicate dots at different rents
                    continue
                seen_prices[key] = rent

    # Build rows from the deduped/lowest-price mapping to feed plotting and CSV
    for (plan, floorplan_id, avail_str, unit_name), rent in seen_prices.items():
        unit_rows.append([
            plan,
            floorplan_id,
            avail_str,
            unit_name,
            rent,
        ])

    if hasattr(progress_iter, "close"):
        progress_iter.close()

    return unit_rows

def ensure_output_dir() -> str:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    return OUTPUT_DIR


def write_unit_csv(unit_rows: List[List], check_start_date: date, check_end_date: date) -> str:
    csv_path = f"{OUTPUT_PREFIX}_{check_start_date}_{check_end_date}.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["floor_plan", "floorplan_id", "availability_date", "unit", "price"])
        writer.writerows(unit_rows)
    return csv_path


def main() -> None:
    check_start_date = date.today()
    check_end_date = check_start_date + timedelta(days=NUM_DAYS)

    ensure_output_dir()
    unit_rows = collect_unit_rows(check_start_date, NUM_DAYS)
    csv_path = write_unit_csv(unit_rows, check_start_date, check_end_date)
    print(f"\nWrote {len(unit_rows)} unit-level rows to {csv_path}")
    plot_unit_prices(unit_rows, OUTPUT_PREFIX, check_start_date, check_end_date)


if __name__ == "__main__":
    main()
