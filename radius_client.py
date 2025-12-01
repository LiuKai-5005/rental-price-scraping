import json
from datetime import datetime
from typing import Dict, List, Tuple

import requests

from models import parse_units


def fetch_housing(start_date: datetime, end_date: datetime) -> Tuple[Dict[str, float], Dict[str, List[list]]]:
    """
    Fetch floor plan pricing and per-unit availability for the given date range.
    Returns a tuple of (price results by plan, mapping of units grouped by plan).
    """
    url = (
        "https://www.essexapartmenthomes.com/"
        "EPT_Feature/PropertyManagement/Service/"
        "GetPropertyAvailabiltyByRange/513957/"
        + str(start_date)[:10]
        + "/"
        + str(end_date)[:10]
    )
    response = requests.get(url)
    houseResponseStr = json.loads(response.content)
    houseResponse = json.loads(houseResponseStr)
    floorPlans = houseResponse["result"]["floorplans"]
    units = parse_units(houseResponse["result"]["units"])
    idMap = {}  # store mapping of floor plan names to IDs

    results: Dict[str, float] = {}
    for plan in floorPlans:
        name = plan["name"]
        if name in {"Ratio", "Locus", "Apex", "Chord"}:
            results[name] = float(plan["minimum_rent"])
            idMap[name] = plan["floorplan_id"]

    mapping: Dict[str, List[list]] = {}
    for unit in units:
        for plan_name, plan_id in idMap.items():
            if unit.floorplan_id == plan_id:
                mapping.setdefault(plan_name, []).append(
                    [unit.floorplan_id, unit.availability_date, unit.name, unit.minimum_rent]
                )
                break

    return results, mapping
