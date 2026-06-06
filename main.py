import streamlit as st

from src.uk_fttp_map.dashboard import (
    render_filters,
    render_insights,
    render_kpis,
    render_map,
    render_methodology,
    render_ranked_table,
)
from src.uk_fttp_map.data import load_boundaries_path, load_metrics
from src.uk_fttp_map.data import DataUnavailableError


st.set_page_config(
    page_title="UK FTTP Opportunity Map",
    layout="wide",
)

st.title("UK FTTP Opportunity Map")
st.caption("Public-data FTTP view focused on premises opportunity.")

try:
    metrics = load_metrics()
    boundaries_path = load_boundaries_path()
except DataUnavailableError as exc:
    st.error("Real public data is unavailable.")
    st.write(str(exc))
    st.info(
        "No regional conclusions should be drawn until the Ofcom FTTP dataset "
        "and ONS boundary file are available. The app does not silently substitute "
        "sample data for production analysis."
    )
    st.stop()

filtered_metrics, selected_metric = render_filters(metrics)

if filtered_metrics.empty:
    st.warning("No postcode districts match the selected filters.")
    st.stop()

render_kpis(filtered_metrics)
render_map(filtered_metrics, selected_metric, boundaries_path)
render_insights(filtered_metrics)
st.subheader("Ranked FTTP opportunities")
render_ranked_table(filtered_metrics)
render_methodology()
