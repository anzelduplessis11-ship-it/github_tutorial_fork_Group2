from __future__ import annotations

import random
from typing import Any, Dict, List


# Small, relatable vocabularies for the school garden / community farm story.
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
WEATHER = ["sunny", "cloudy", "rainy"]
CROPS = ["maize", "beans", "tomato", "spinach"]


def _decide_water_need(weather: str, temperature_c: float, soil_moisture: float, rainfall_mm: float) -> str:
    """
    Turn the weather-and-soil observation into a simple water label.

    This is a soft rule, not a lookup table: hot + dry soil pushes toward
    "high", while wet soil or fresh rainfall pushes toward "low".
    """
    score = 0.0
    score += (temperature_c - 25) * 0.15      # hotter -> needs more water
    score += (40 - soil_moisture) * 0.08      # drier soil -> needs more water
    score -= rainfall_mm * 0.12               # recent rain -> needs less water
    if weather == "sunny":
        score += 0.8
    elif weather == "rainy":
        score -= 0.8

    if score > 1.5:
        return "high"
    if score < -0.5:
        return "low"
    return "medium"


def fetch_event_data(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create or load the controlled synthetic dataset for the workshop pipeline.

    Input contract:
    - config["dataset_name"]: human-friendly name for the dataset.
    - config["source"]: should be the string "synthetic" for this starter repo.
    - config["limit"]: optional maximum number of rows to keep.

    Output contract:
    - dataset_name: str
    - source: str
    - records: list[dict]
    - notes: list[str]

    Suggested beginner story:
    - use a fictional school garden / community farm story
    - keep one row per weather-and-soil observation
    - do not change the output keys
    """
    dataset_name = config.get("dataset_name", "school_garden_water_need")
    source = config.get("source", "synthetic")

    # A default that gives the model enough rows to learn from.
    limit = config.get("limit")
    total_rows = 200 if limit is None else max(int(limit), 0)

    # Fixed seed so every group generates the exact same controlled dataset.
    rng = random.Random(42)

    records: List[Dict[str, Any]] = []
    for _ in range(total_rows):
        weather = rng.choice(WEATHER)
        temperature_c = rng.randint(18, 38)
        # Rainy days tend to bring more rainfall and wetter soil.
        rainfall_mm = rng.randint(10, 30) if weather == "rainy" else rng.randint(0, 6)
        soil_moisture = rng.randint(10, 80)
        crop_type = rng.choice(CROPS)

        record = {
            "day_of_week": rng.choice(DAYS),
            "weather": weather,
            "temperature_c": temperature_c,
            "rainfall_mm": rainfall_mm,
            "soil_moisture": soil_moisture,
            "crop_type": crop_type,
            "water_need": _decide_water_need(weather, temperature_c, soil_moisture, rainfall_mm),
        }
        records.append(record)

    notes = [
        f"Synthetic school garden dataset with {len(records)} observations.",
        "One row per weather-and-soil observation for a fictional community farm.",
        "Target is water_need with classes: low, medium, high.",
        "Data is generated with a fixed random seed so results are reproducible.",
    ]

    return {
        "dataset_name": dataset_name,
        "source": source,
        "records": records,
        "notes": notes,
    }
