import streamlit as st

st.set_page_config(page_title="Departure Airfield", page_icon="🛫")
st.markdown("# Departure Airfield")
st.sidebar.header("Departure Airfield")
st.write(
    """Enter airfield details, weather condition and aircraft weight at the place of departure."""
)

if 'cache' not in st.session_state:
    st.session_state["cache"] = {}
metrics = [
    "departure_airfield_name",
    "departure_airfield_code",
    "departure_airfield_elevation",
    "departure_rw_heading",
    "departure_fuel",
    "departure_qnh",
    "departure_oat",
    "departure_wind_speed",
    "departure_wind_direction",
]
for metric in metrics:
    if metric not in st.session_state["cache"]:
        if metric in ("departure_airfield_name", "departure_airfield_code"):
            st.session_state["cache"][metric] = ""
        else:
            st.session_state["cache"][metric] = 0

st.session_state["cache"]["departure_airfield_name"] = st.text_input(
    label="Airfield Name",
    placeholder="Hof",
    key="departure_airfield_name",
    value=st.session_state["cache"]["departure_airfield_name"]
)
st.session_state["cache"]["departure_airfield_code"] = st.text_input(
    label="ICAO Code",
    placeholder="EDQM",
    key="departure_airfield_code",
    value=st.session_state["cache"]["departure_airfield_code"]
)
st.session_state["cache"]["departure_airfield_elevation"] = st.number_input(
    label="Airfield Elevation (ft)",
    placeholder="1342",
    key="departure_airfield_elevation",
    step=1,
    value=st.session_state["cache"]["departure_airfield_elevation"]
)
st.session_state["cache"]["departure_rw_heading"] = st.number_input(
    label="Runway Heading (°)",
    placeholder="260",
    key="departure_rw_heading",
    step=1,
    value=st.session_state["cache"]["departure_rw_heading"]
)
st.session_state["cache"]["departure_fuel"] = st.number_input(
    label="Fuel (l)",
    placeholder="70",
    key="departure_fuel",
    step=1,
    value=st.session_state["cache"]["departure_fuel"]
)
st.session_state["cache"]["departure_qnh"] = st.number_input(
    label="QNH (hPa)",
    placeholder="1017",
    key="departure_qnh",
    step=1,
    value=st.session_state["cache"]["departure_qnh"]
)
st.session_state["cache"]["departure_oat"] = st.number_input(
    label="OAT (°C)",
    placeholder="23",
    key="departure_oat",
    step=1,
    value=st.session_state["cache"]["departure_oat"]
)
st.session_state["cache"]["departure_wind_speed"] = st.number_input(
    label="Wind Speed (kt)",
    placeholder="11",
    key="departure_wind_speed",
    step=1,
    value=st.session_state["cache"]["departure_wind_speed"]
)
st.session_state["cache"]["departure_wind_direction"] = st.number_input(
    label="Wind Direction (°)",
    placeholder="290",
    key="departure_wind_direction",
    step=1,
    value=st.session_state["cache"]["departure_wind_direction"]
)

