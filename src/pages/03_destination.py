import streamlit as st

st.set_page_config(page_title="Departure Airfield", page_icon="🛬")
st.markdown("# Destination Airfield")
st.sidebar.header("Destination Airfield")
st.write(
    """Enter airfield details, weather condition and aircraft weight at your planned destination."""
)

if 'cache' not in st.session_state:
    st.session_state["cache"] = {}
metrics = [
    "destination_airfield_name",
    "destination_airfield_code",
    "destination_airfield_elevation",
    "destination_rw_heading",
    "destination_fuel",
    "destination_qnh",
    "destination_oat",
    "destination_wind_speed",
    "destination_wind_direction",
]
for metric in metrics:
    if metric not in st.session_state["cache"]:
        if metric in ("destination_airfield_name", "destination_airfield_code"):
            st.session_state["cache"][metric] = ""
        else:
            st.session_state["cache"][metric] = 0

st.session_state["cache"]["destination_airfield_name"] = st.text_input(
    label="Airfield Name",
    placeholder="Hof",
    key="destination_airfield_name",
    value=st.session_state["cache"]["destination_airfield_name"]
)
st.session_state["cache"]["destination_airfield_code"] = st.text_input(
    label="ICAO Code",
    placeholder="EDQM",
    key="destination_airfield_code",
    value=st.session_state["cache"]["destination_airfield_code"]
)
st.session_state["cache"]["destination_airfield_elevation"] = st.number_input(
    label="Airfield Elevation (ft)",
    placeholder="1342",
    key="destination_airfield_elevation",
    step=1,
    value=st.session_state["cache"]["destination_airfield_elevation"]
)
st.session_state["cache"]["destination_rw_heading"] = st.number_input(
    label="Runway Heading (°)",
    placeholder="260",
    key="destination_rw_heading",
    step=1,
    value=st.session_state["cache"]["destination_rw_heading"]
)
st.session_state["cache"]["destination_fuel"] = st.number_input(
    label="Fuel (l)",
    placeholder="70",
    key="destination_fuel",
    step=1,
    value=st.session_state["cache"]["destination_fuel"]
)
st.session_state["cache"]["destination_qnh"] = st.number_input(
    label="QNH (hPa)",
    placeholder="1017",
    key="destination_qnh",
    step=1,
    value=st.session_state["cache"]["destination_qnh"]
)
st.session_state["cache"]["destination_oat"] = st.number_input(
    label="OAT (°C)",
    placeholder="23",
    key="destination_oat",
    step=1,
    value=st.session_state["cache"]["destination_oat"]
)
st.session_state["cache"]["destination_wind_speed"] = st.number_input(
    label="Wind Speed (kt)",
    placeholder="11",
    key="destination_wind_speed",
    step=1,
    value=st.session_state["cache"]["destination_wind_speed"]
)

st.session_state["cache"]["destination_wind_direction"] = st.number_input(
    label="Wind Direction (°)",
    placeholder="290",
    key="destination_wind_direction",
    step=1,
    value=0 if not (isinstance(st.session_state["cache"]["destination_wind_direction"], float) or isinstance(st.session_state["cache"]["destination_wind_direction"], int)) else st.session_state["cache"]["destination_wind_direction"]
)
