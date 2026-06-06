import streamlit as st

from src.uk_fttp_map.dashboard import (
    render_filters,
    render_kpis,
    render_map,
    render_methodology,
    render_ranked_table,
)
from src.uk_fttp_map.data import load_boundaries_path, load_metrics


st.set_page_config(
    page_title="UK FTTP Opportunity Map",
    layout="wide",
)

st.title("UK FTTP Opportunity Map")
st.caption("Public-data postcode district view focused on full fibre premises opportunity.")

metrics = load_metrics()
filtered_metrics, selected_metric = render_filters(metrics)

if filtered_metrics.empty:
    st.warning("No postcode districts match the selected filters.")
    st.stop()

render_kpis(filtered_metrics)
render_map(filtered_metrics, selected_metric, load_boundaries_path())
st.subheader("Ranked postcode district opportunities")
render_ranked_table(filtered_metrics)
render_methodology()
