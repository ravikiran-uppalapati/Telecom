import pandas as pd

from src.uk_fttp_map.scoring import assign_category, calculate_metrics, score_opportunities


def test_calculate_metrics_adds_non_fttp_and_coverage():
    df = pd.DataFrame(
        {
            "postcode_district": ["M1"],
            "total_premises": [1000],
            "fttp_available_premises": [250],
            "area_sq_km": [2.0],
        }
    )

    result = calculate_metrics(df)

    assert result.loc[0, "non_fttp_premises"] == 750
    assert result.loc[0, "fttp_coverage_percent"] == 25.0
    assert result.loc[0, "premises_density"] == 500.0


def test_score_opportunities_uses_expected_weighting():
    df = pd.DataFrame(
        {
            "postcode_district": ["A1", "B1"],
            "total_premises": [1000, 1000],
            "fttp_available_premises": [900, 100],
            "area_sq_km": [10.0, 1.0],
        }
    )

    result = score_opportunities(calculate_metrics(df))

    b_score = result.loc[result["postcode_district"] == "B1", "opportunity_score"].iloc[0]
    a_score = result.loc[result["postcode_district"] == "A1", "opportunity_score"].iloc[0]
    assert b_score > a_score


def test_assign_category_prioritises_dense_low_coverage():
    category = assign_category(
        fttp_coverage_percent=20.0,
        non_fttp_premises=900,
        premises_density=1200.0,
        opportunity_score=85.0,
    )

    assert category == "Dense priority"
