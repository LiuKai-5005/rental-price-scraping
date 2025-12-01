from dataclasses import dataclass
from datetime import datetime
from typing import Any, List, Optional


@dataclass
class Unit:
    unit_id: int
    floorplan_id: int
    name: str
    beds: float
    baths: float
    sqft: int
    deposit: float
    availability_date: Optional[datetime]
    minimum_rent: float
    maximum_rent: float
    make_ready_date: Optional[datetime]
    aging_days: int
    hold_days: int


def parse_iso_datetime(dt_str: Optional[str]) -> Optional[datetime]:
    if not dt_str:
        return None
    if dt_str.endswith("Z"):
        dt_str = dt_str.replace("Z", "+00:00")
    return datetime.fromisoformat(dt_str)


def parse_units(payload: List[dict[str, Any]]) -> List[Unit]:
    """
    Convert the raw payload (list of dicts) into a list of Unit objects.
    """
    units: List[Unit] = []

    for item in payload:
        unit = Unit(
            unit_id=int(item["unit_id"]),
            floorplan_id=int(item["floorplan_id"]),
            name=str(item["name"]),
            beds=float(item["beds"]),
            baths=float(item["baths"]),
            sqft=int(item["sqft"]),
            deposit=float(item["deposit"]),
            availability_date=parse_iso_datetime(item.get("availability_date")),
            minimum_rent=float(item["minimum_rent"]),
            maximum_rent=float(item["maximum_rent"]),
            make_ready_date=parse_iso_datetime(item.get("make_ready_date")),
            aging_days=int(item["aging_days"]),
            hold_days=int(item["hold_days"]),
        )
        units.append(unit)

    return units
