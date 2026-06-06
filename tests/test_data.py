import pandas as pd
import pytest

from src.uk_fttp_map.data import REQUIRED_METRIC_COLUMNS, load_metrics, validate_metrics


def test_validate_metrics_accepts_required_columns():
    df = pd.DataFrame(
        {
            "postcode_district": ["M1"],
            "nation": ["England"],
            "region": ["North West"],
            "total_premises": [100],
            "fttp_available_premises": [50],
            "area_sq_km": [1.0],
        }
    )

    validate_metrics(df)


def test_validate_metrics_rejects_missing_columns():
    df = pd.DataFrame({"postcode_district": ["M1"]})

    with pytest.raises(ValueError, match="Missing required columns"):
        validate_metrics(df)


def test_load_metrics_returns_scored_rows():
    df = load_metrics()

    assert set(REQUIRED_METRIC_COLUMNS).issubset(df.columns)
    assert "opportunity_score" in df.columns
    assert "opportunity_category" in df.columns
    assert len(df) >= 6
