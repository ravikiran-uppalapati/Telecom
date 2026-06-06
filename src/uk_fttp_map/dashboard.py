from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


METRIC_OPTIONS = {
    "Opportunity score": "opportunity_score",
    "FTTP coverage %": "fttp_coverage_percent",
    "Premises without FTTP": "non_fttp_premises",
    "Premises density": "premises_density",
}


def render_filters(df: pd.DataFrame) -> tuple[pd.DataFrame, str]:
    with st.sidebar:
        st.header("Filters")
        metric_label = st.selectbox("Map metric", list(METRIC_OPTIONS.keys()))
        nations = sorted(df["nation"].dropna().unique())
        selected_nations = st.multiselect("Nation", nations, default=nations)
        categories = sorted(df["opportunity_category"].dropna().unique())
        selected_categories = st.multiselect(
            "Opportunity category",
            categories,
            default=categories,
        )
        min_premises = st.slider(
            "Minimum total premises",
            min_value=0,
            max_value=int(df["total_premises"].max()),
            value=0,
            step=100,
        )

    filtered = df[
        df["nation"].isin(selected_nations)
        & df["opportunity_category"].isin(selected_categories)
        & (df["total_premises"] >= min_premises)
    ].copy()
    return filtered, METRIC_OPTIONS[metric_label]


def render_kpis(df: pd.DataFrame) -> None:
    total_premises = int(df["total_premises"].sum())
    non_fttp = int(df["non_fttp_premises"].sum())
    weighted_coverage = 0.0
    if total_premises:
        weighted_coverage = (
            df["fttp_available_premises"].sum() / total_premises * 100
        )

    col1, col2, col3 = st.columns(3)
    col1.metric("Total premises", f"{total_premises:,.0f}")
    col2.metric("Premises without FTTP", f"{non_fttp:,.0f}")
    col3.metric("Weighted FTTP coverage", f"{weighted_coverage:.1f}%")


def render_map(df: pd.DataFrame, metric: str, boundaries_path: Path) -> None:
    geojson = json.loads(boundaries_path.read_text())
    fig = px.choropleth_map(
        df,
        geojson=geojson,
        locations="postcode_district",
        featureidkey="properties.postcode_district",
        color=metric,
        hover_name="postcode_district",
        hover_data={
            "nation": True,
            "region": True,
            "total_premises": ":,",
            "non_fttp_premises": ":,",
            "fttp_coverage_percent": ":.1f",
            "opportunity_category": True,
        },
        map_style="carto-positron",
        center={"lat": 54.5, "lon": -3.0},
        zoom=4.2,
        opacity=0.72,
        color_continuous_scale="Viridis",
    )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=560)
    st.plotly_chart(fig, use_container_width=True)


def render_ranked_table(df: pd.DataFrame) -> None:
    columns = [
        "postcode_district",
        "nation",
        "region",
        "total_premises",
        "fttp_available_premises",
        "non_fttp_premises",
        "fttp_coverage_percent",
        "premises_density",
        "opportunity_score",
        "opportunity_category",
    ]
    st.dataframe(df[columns], use_container_width=True, hide_index=True)

    csv = df[columns].to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download CSV",
        data=csv,
        file_name="uk_fttp_postcode_district_opportunities.csv",
        mime="text/csv",
    )


def render_methodology() -> None:
    with st.expander("Methodology and limitations"):
        st.write(
            "This version uses public/sample FTTP premises data at postcode district level. "
            "The opportunity score is premises-led: 50% non-FTTP premises, "
            "30% inverse FTTP coverage, and 20% premises density. "
            "Copper, ADSL, PSTN, and FTTC-only coverage are out of scope."
        )
