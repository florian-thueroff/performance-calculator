import streamlit as st
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(page_title="Alternate Airfield", page_icon="✈️")
st.markdown("# Alternate Airfield")
st.sidebar.header("Alternate Airfield")
st.write(
    """Enter airfield details, weather condition and aircraft weight at the alternate airfield."""
)

if 'cache' not in st.session_state:
    st.session_state["cache"] = {}
metrics = [
    "alternate_airfield_name",
    "alternate_airfield_code",
    "alternate_airfield_elevation",
    "alternate_rw_heading",
    "alternate_fuel",
    "alternate_qnh",
    "alternate_oat",
    "alternate_wind_speed",
    "alternate_wind_direction",
]
for metric in metrics:
    if metric not in st.session_state["cache"]:
        if metric in ("alternate_airfield_name", "alternate_airfield_code"):
            st.session_state["cache"][metric] = ""
        else:
            st.session_state["cache"][metric] = 0

st.session_state["cache"]["alternate_airfield_name"] = st.text_input(
    label="Airfield Name",
    placeholder="Hof",
    key="alternate_airfield_name",
    value=st.session_state["cache"]["alternate_airfield_name"]
)
st.session_state["cache"]["alternate_airfield_code"] = st.text_input(
    label="ICAO Code",
    placeholder="EDQM",
    key="alternate_airfield_code",
    value=st.session_state["cache"]["alternate_airfield_code"]
)
st.session_state["cache"]["alternate_airfield_elevation"] = st.number_input(
    label="Airfield Elevation (ft)",
    placeholder="1342",
    key="alternate_airfield_elevation",
    step=1,
    value=st.session_state["cache"]["alternate_airfield_elevation"]
)
st.session_state["cache"]["alternate_rw_heading"] = st.number_input(
    label="Runway Heading (°)",
    placeholder="260",
    key="alternate_rw_heading",
    step=1,
    value=st.session_state["cache"]["alternate_rw_heading"]
)
st.session_state["cache"]["alternate_fuel"] = st.number_input(
    label="Fuel (l)",
    placeholder="70",
    key="alternate_fuel",
    step=1,
    value=st.session_state["cache"]["alternate_fuel"]
)
st.session_state["cache"]["alternate_qnh"] = st.number_input(
    label="QNH (hPa)",
    placeholder="1017",
    key="alternate_qnh",
    step=1,
    value=st.session_state["cache"]["alternate_qnh"]
)
st.session_state["cache"]["alternate_oat"] = st.number_input(
    label="OAT (°C)",
    placeholder="23",
    key="alternate_oat",
    step=1,
    value=st.session_state["cache"]["alternate_oat"]
)
st.session_state["cache"]["alternate_wind_speed"] = st.number_input(
    label="Wind Speed (kt)",
    placeholder="11",
    key="alternate_wind_speed",
    step=1,
    value=st.session_state["cache"]["alternate_wind_speed"]
)
st.session_state["cache"]["alternate_wind_direction"] = st.number_input(
    label="Wind Direction (°)",
    placeholder="290",
    key="alternate_wind_direction",
    step=1,
    value=st.session_state["cache"]["alternate_wind_direction"]
)

summary = st.button(
    label="Inspect Results",
    type="primary"
)
if summary:
    switch_page("summary")
