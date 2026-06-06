from __future__ import annotations

from pathlib import Path
from urllib.request import urlretrieve


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CACHE_DIR = PROJECT_ROOT / "data" / "cache"

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


def download_file(url: str, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    urlretrieve(url, destination)


def main() -> None:
    downloads = [
        (OFCOM_FIXED_BROADBAND_URL, CACHE_DIR / "ofcom_fixed_broadband_202601.zip"),
        (ONS_LAUA_BOUNDARIES_URL, CACHE_DIR / "laua_boundaries_dec_2025.geojson"),
    ]
    for url, destination in downloads:
        print(f"Downloading {destination.name}...")
        download_file(url, destination)
    print("Real public data cached in data/cache.")


if __name__ == "__main__":
    main()
