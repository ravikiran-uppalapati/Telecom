from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.uk_fttp_map.scoring import calculate_metrics, score_opportunities


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SAMPLE_METRICS_PATH = PROJECT_ROOT / "data" / "sample" / "postcode_district_metrics.csv"
SAMPLE_BOUNDARIES_PATH = PROJECT_ROOT / "data" / "sample" / "postcode_district_boundaries.geojson"

REQUIRED_METRIC_COLUMNS = [
    "postcode_district",
    "nation",
    "region",
    "total_premises",
    "fttp_available_premises",
    "area_sq_km",
]


def validate_metrics(df: pd.DataFrame) -> None:
    missing = [column for column in REQUIRED_METRIC_COLUMNS if column not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")

    numeric_columns = ["total_premises", "fttp_available_premises", "area_sq_km"]
    for column in numeric_columns:
        if (df[column] < 0).any():
            raise ValueError(f"{column} cannot contain negative values")


def load_metrics(path: Path | str = SAMPLE_METRICS_PATH) -> pd.DataFrame:
    df = pd.read_csv(path)
    validate_metrics(df)
    scored = score_opportunities(calculate_metrics(df))
    return scored.sort_values("opportunity_score", ascending=False).reset_index(drop=True)


def load_boundaries_path() -> Path:
    return SAMPLE_BOUNDARIES_PATH
