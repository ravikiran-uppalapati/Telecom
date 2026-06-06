import re


POSTCODE_DISTRICT_RE = re.compile(r"^([A-Z]{1,2}[0-9][A-Z0-9]?)")


def _compact(value: str) -> str:
    return re.sub(r"\s+", "", value.strip().upper())


def extract_postcode_district(postcode: str) -> str:
    if not isinstance(postcode, str):
        raise ValueError("postcode must be a string")

    compacted = _compact(postcode)
    if len(compacted) <= 3:
        raise ValueError(f"invalid UK postcode: {postcode!r}")

    district = compacted[:-3]
    return normalise_postcode_district(district)


def normalise_postcode_district(district: str) -> str:
    if not isinstance(district, str):
        raise ValueError("postcode district must be a string")

    compacted = _compact(district)
    if not POSTCODE_DISTRICT_RE.fullmatch(compacted):
        raise ValueError(f"invalid UK postcode district: {district!r}")
    return compacted
