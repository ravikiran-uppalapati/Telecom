import pytest

from src.uk_fttp_map.postcodes import extract_postcode_district, normalise_postcode_district


@pytest.mark.parametrize(
    ("postcode", "expected"),
    [
        ("SW1A 1AA", "SW1A"),
        ("sw1a1aa", "SW1A"),
        ("M1 1AE", "M1"),
        ("B15 2TT", "B15"),
        ("EC1A 1BB", "EC1A"),
        ("W1A 0AX", "W1A"),
    ],
)
def test_extract_postcode_district(postcode, expected):
    assert extract_postcode_district(postcode) == expected


@pytest.mark.parametrize(
    ("district", "expected"),
    [
        (" sw1a ", "SW1A"),
        ("m1", "M1"),
        ("B15", "B15"),
    ],
)
def test_normalise_postcode_district(district, expected):
    assert normalise_postcode_district(district) == expected


@pytest.mark.parametrize("value", ["", None, "NOT A POSTCODE", "12345"])
def test_extract_postcode_district_rejects_invalid_values(value):
    with pytest.raises(ValueError):
        extract_postcode_district(value)
