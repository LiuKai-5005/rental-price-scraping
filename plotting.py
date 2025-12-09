from datetime import datetime
from typing import List

import matplotlib.pyplot as plt


def plot_unit_prices(unit_rows: List[List], output_prefix: str, check_start_date, check_end_date) -> None:
    """
    Plot per-unit prices against move-in dates and save a PNG.
    """
    plot_points: dict[str, list[tuple[datetime, float, str]]] = {
        "Ratio": [],
        "Locus": [],
        "Apex": [],
        "Chord": [],
    }
    seen_points = set()  # guard against duplicated rows in the input

    for plan, _, avail_date, unit_name, price in unit_rows:
        if not avail_date:
            continue
        try:
            move_in_date = datetime.fromisoformat(str(avail_date))
        except ValueError:
            continue
        # Only show one point per plan/unit/date to avoid duplicate dots when prices vary
        dedup_key = (plan, move_in_date, unit_name)
        if dedup_key in seen_points:
            continue
        seen_points.add(dedup_key)
        if plan not in plot_points:
            plot_points[plan] = []
        plot_points[plan].append((move_in_date, price, unit_name))

    plt.rcParams.update({"font.size": 16})
    plt.figure(figsize=(18, 6))
    styles = {
        "Ratio": ("o", "blue", "Ratio"),
        "Locus": ("+", "green", "Locus"),
        "Apex": ("x", "red", "Apex"),
        "Chord": ("s", "magenta", "Chord"),
    }

    plotted = False
    for plan, points in plot_points.items():
        if not points:
            continue
        dates_list = [p[0] for p in points]
        prices_list = [p[1] for p in points]
        unit_names = [p[2] for p in points]
        marker, color, label = styles.get(plan, ("o", None, plan))
        plt.scatter(dates_list, prices_list, marker=marker, color=color, label=label)
        for x, y, unit_name in zip(dates_list, prices_list, unit_names):
            plt.annotate(
                unit_name,
                (x, y),
                textcoords="offset points",
                xytext=(6, 8),
                fontsize=14,
                color="navy",
                fontweight="bold",
            )
            plt.annotate(
                f"${y:,.0f}",
                (x, y),
                textcoords="offset points",
                xytext=(6, -6),
                fontsize=13,
                color="darkorange",
            )
        plotted = True

    if plotted:
        plt.xlabel("Move-in Dates")
        plt.ylabel("Unit Prices ($)")
        plt.legend()
        plt.title("Radius rental prices by floor plan (per unit)")
        plt.savefig(f"{output_prefix}_{check_start_date}_{check_end_date}.png")
