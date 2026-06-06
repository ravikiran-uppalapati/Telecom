from zipfile import ZipFile

import pandas as pd
import pytest

from src.uk_fttp_map.data import (
    REQUIRED_METRIC_COLUMNS,
    load_metrics,
    load_ofcom_laua_metrics,
    validate_metrics,
)


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


def test_load_ofcom_laua_metrics_maps_real_fttp_columns(tmp_path):
    zip_path = tmp_path / "ofcom.zip"
    csv_path = "202601_fixed_laua_coverage_r1/202601_fixed_laua_coverage_r1.csv"
    csv_text = "\n".join(
        [
            "laua,laua_name,All Premises,Number of premises with Full Fibre availability",
            "E06000001,Hartlepool,50000,25000",
            "S12000033,Aberdeen City,132364,123173",
        ]
    )
    with ZipFile(zip_path, "w") as archive:
        archive.writestr(csv_path, csv_text)

    df = load_ofcom_laua_metrics(zip_path)

    assert list(df["postcode_district"]) == ["E06000001", "S12000033"]
    assert list(df["region"]) == ["Hartlepool", "Aberdeen City"]
    assert list(df["total_premises"]) == [50000, 132364]
    assert list(df["fttp_available_premises"]) == [25000, 123173]
    assert "opportunity_score" in df.columns
