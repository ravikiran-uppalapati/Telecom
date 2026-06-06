from __future__ import annotations

from src.uk_fttp_map.data import ensure_public_data_cached


def main() -> None:
    ensure_public_data_cached()
    print("Real public data cached in data/cache.")


if __name__ == "__main__":
    main()
