from __future__ import annotations

from pathlib import Path
from urllib.request import urlretrieve
from zipfile import ZipFile

import pandas as pd

from src.uk_fttp_map.scoring import calculate_metrics, score_opportunities


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SAMPLE_METRICS_PATH = PROJECT_ROOT / "data" / "sample" / "postcode_district_metrics.csv"
SAMPLE_BOUNDARIES_PATH = PROJECT_ROOT / "data" / "sample" / "postcode_district_boundaries.geojson"
PUBLIC_METRICS_PATH = PROJECT_ROOT / "data" / "public" / "ofcom_laua_fttp_metrics_202601.csv"
PUBLIC_BOUNDARIES_PATH = PROJECT_ROOT / "data" / "public" / "laua_boundaries_dec_2025.geojson"
OFCOM_FIXED_BROADBAND_ZIP_PATH = PROJECT_ROOT / "data" / "cache" / "ofcom_fixed_broadband_202601.zip"
LAUA_BOUNDARIES_PATH = PROJECT_ROOT / "data" / "cache" / "laua_boundaries_dec_2025.geojson"
OFCOM_FIXED_BROADBAND_URL = (
    "https://www.ofcom.org.uk/siteassets/resources/documents/research-and-data/"
    "multi-sector/infrastructure-research/connected-nations-spring-2026/"
    "202601_fixed_broadband_coverage_and_full_fibre_take-up-r1.zip?v=417689"
)
ONS_LAUA_BOUNDARIES_URL = (
    "https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/"
    "Local_Authority_Districts_DEC_2025_Boundaries_UK_BGC/FeatureServer/0/query"
    "?where=1%3D1&outFields=LAD25CD,LAD25NM&outSR=4326&f=geojson"
)

REQUIRED_METRIC_COLUMNS = [
    "postcode_district",
    "nation",
    "region",
    "total_premises",
    "fttp_available_premises",
    "area_sq_km",
]


class DataUnavailableError(RuntimeError):
    """Raised when required public data cannot be loaded."""


def validate_metrics(df: pd.DataFrame) -> None:
    missing = [column for column in REQUIRED_METRIC_COLUMNS if column not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")

    numeric_columns = ["total_premises", "fttp_available_premises", "area_sq_km"]
    for column in numeric_columns:
        if (df[column] < 0).any():
            raise ValueError(f"{column} cannot contain negative values")


def _score_and_sort(df: pd.DataFrame) -> pd.DataFrame:
    scored = score_opportunities(calculate_metrics(df))
    return scored.sort_values("opportunity_score", ascending=False).reset_index(drop=True)


def _nation_from_laua(code: str) -> str:
    if code.startswith("E"):
        return "England"
    if code.startswith("S"):
        return "Scotland"
    if code.startswith("W"):
        return "Wales"
    if code.startswith("N"):
        return "Northern Ireland"
    return "Unknown"


def download_file(url: str, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    urlretrieve(url, destination)


def ensure_public_data_cached() -> None:
    if PUBLIC_METRICS_PATH.exists() and PUBLIC_BOUNDARIES_PATH.exists():
        return

    downloads = [
        (OFCOM_FIXED_BROADBAND_URL, OFCOM_FIXED_BROADBAND_ZIP_PATH),
        (ONS_LAUA_BOUNDARIES_URL, LAUA_BOUNDARIES_PATH),
    ]
    for url, destination in downloads:
        if not destination.exists():
            download_file(url, destination)


def load_ofcom_laua_metrics(zip_path: Path | str = OFCOM_FIXED_BROADBAND_ZIP_PATH) -> pd.DataFrame:
    csv_name = "202601_fixed_laua_coverage_r1/202601_fixed_laua_coverage_r1.csv"
    with ZipFile(zip_path) as archive:
        df = pd.read_csv(archive.open(csv_name), encoding="latin1")

    result = pd.DataFrame(
        {
            "postcode_district": df["laua"].astype(str),
            "area_name": df["laua_name"].astype(str).str.title(),
            "geography_level": "Local authority",
            "nation": df["laua"].astype(str).map(_nation_from_laua),
            "region": df["laua_name"].astype(str).str.title(),
            "total_premises": pd.to_numeric(df["All Premises"], errors="coerce").fillna(0),
            "fttp_available_premises": pd.to_numeric(
                df["Number of premises with Full Fibre availability"],
                errors="coerce",
            ).fillna(0),
            "area_sq_km": 0.0,
        }
    )
    validate_metrics(result)
    return _score_and_sort(result)


def load_demo_metrics(path: Path | str = SAMPLE_METRICS_PATH) -> pd.DataFrame:
    df = pd.read_csv(path)
    validate_metrics(df)
    df["area_name"] = df.get("area_name", df["postcode_district"])
    df["geography_level"] = "Postcode district demo"
    return _score_and_sort(df)


def load_metrics(path: Path | str | None = None) -> pd.DataFrame:
    if path is None:
        if PUBLIC_METRICS_PATH.exists():
            return load_metrics(PUBLIC_METRICS_PATH)

        try:
            ensure_public_data_cached()
        except OSError as exc:
            raise DataUnavailableError(
                "The public FTTP data is unavailable. The app could not download "
                "the Ofcom Spring 2026 fixed broadband dataset or ONS boundary file."
            ) from exc

        if not OFCOM_FIXED_BROADBAND_ZIP_PATH.exists():
            raise DataUnavailableError(
                "The public FTTP data is unavailable. The Ofcom Spring 2026 fixed "
                "broadband dataset is missing from data/cache."
            )
        return load_ofcom_laua_metrics(OFCOM_FIXED_BROADBAND_ZIP_PATH)

    df = pd.read_csv(path)
    validate_metrics(df)
    if "area_name" not in df.columns:
        df["area_name"] = df["postcode_district"]
    if "geography_level" not in df.columns:
        df["geography_level"] = "Postcode district sample"
    return _score_and_sort(df)


def load_boundaries_path() -> Path:
    if PUBLIC_BOUNDARIES_PATH.exists():
        return PUBLIC_BOUNDARIES_PATH

    try:
        ensure_public_data_cached()
    except OSError as exc:
        raise DataUnavailableError(
            "The public FTTP boundaries are unavailable. The app could not download "
            "the ONS December 2025 local-authority boundary file."
        ) from exc
    if not LAUA_BOUNDARIES_PATH.exists():
        raise DataUnavailableError(
            "The public FTTP boundaries are unavailable. The ONS local-authority "
            "boundary file is missing from data/cache."
        )
    return LAUA_BOUNDARIES_PATH
