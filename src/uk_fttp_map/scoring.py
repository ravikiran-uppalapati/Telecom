from __future__ import annotations

import pandas as pd


def _normalise(series: pd.Series) -> pd.Series:
    minimum = series.min()
    maximum = series.max()
    if pd.isna(minimum) or pd.isna(maximum) or maximum == minimum:
        return pd.Series([0.0] * len(series), index=series.index)
    return (series - minimum) / (maximum - minimum)


def calculate_metrics(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    result["non_fttp_premises"] = (
        result["total_premises"] - result["fttp_available_premises"]
    ).clip(lower=0)
    result["fttp_coverage_percent"] = (
        result["fttp_available_premises"] / result["total_premises"] * 100
    ).fillna(0.0)
    area = pd.to_numeric(result["area_sq_km"], errors="coerce")
    density = result["total_premises"] / area.where(area > 0)
    result["premises_density"] = density.fillna(0.0)
    return result


def assign_category(
    *,
    fttp_coverage_percent: float,
    non_fttp_premises: int,
    premises_density: float,
    opportunity_score: float,
) -> str:
    if fttp_coverage_percent >= 85 and non_fttp_premises < 500:
        return "Full-fibre strong"
    if fttp_coverage_percent < 40 and premises_density >= 750:
        return "Dense priority"
    if non_fttp_premises >= 5000:
        return "Major opportunity"
    if fttp_coverage_percent < 40:
        return "Fibre gap"
    if fttp_coverage_percent < 75:
        return "Moderate coverage"
    if opportunity_score < 25:
        return "Lower priority"
    return "Moderate coverage"


def score_opportunities(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    non_fttp_score = _normalise(result["non_fttp_premises"])
    inverse_coverage_score = 1 - (result["fttp_coverage_percent"].clip(0, 100) / 100)
    density_score = _normalise(result["premises_density"])

    result["opportunity_score"] = (
        (0.5 * non_fttp_score)
        + (0.3 * inverse_coverage_score)
        + (0.2 * density_score)
    ) * 100
    result["opportunity_score"] = result["opportunity_score"].round(2)

    result["opportunity_category"] = result.apply(
        lambda row: assign_category(
            fttp_coverage_percent=float(row["fttp_coverage_percent"]),
            non_fttp_premises=int(row["non_fttp_premises"]),
            premises_density=float(row["premises_density"]),
            opportunity_score=float(row["opportunity_score"]),
        ),
        axis=1,
    )
    return result
