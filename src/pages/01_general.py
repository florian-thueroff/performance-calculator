import streamlit as st

st.set_page_config(page_title="General Information", page_icon="✏️")
st.markdown("# General Information")
st.sidebar.header("General Information")
st.write(
    """Enter general planning information."""
)

if 'cache' not in st.session_state:
    st.session_state["cache"] = {}
metrics = [
    "departure_time",
    "arrival_time",
    "pilot_weight",
    "passenger_weight",
    "baggage_weight",
    "safety_margin",
]
for metric in metrics:
    if metric not in st.session_state["cache"]:
        if metric in ("departure_time", "arrival_time"):
            st.session_state["cache"][metric] = ""
        else:
            st.session_state["cache"][metric] = 0

st.session_state["cache"]["departure_time"] = st.text_input(
    label="Planned Departure Time (UTC)",
    placeholder="10:00",
    key="departure_time",
    value=st.session_state["cache"]["departure_time"],
)
st.session_state["cache"]["arrival_time"] = st.text_input(
    label="Planned Arrival Time (UTC)",
    placeholder="11:30",
    key="arrival_time",
    value=st.session_state["cache"]["arrival_time"],
)
st.session_state["cache"]["pilot_weight"] = st.number_input(
    label="Pilot Weight (kg)",
    placeholder="85",
    key="pilot_weight",
    value=st.session_state["cache"]["pilot_weight"],
)
st.session_state["cache"]["passenger_weight"] = st.number_input(
    label="Passenger Weight (kg)",
    placeholder="55",
    key="passenger_weight",
    value=st.session_state["cache"]["passenger_weight"],
)
st.session_state["cache"]["baggage_weight"] = st.number_input(
    label="Baggage Weight (kg)",
    placeholder="15",
    key="baggage_weight",
    value=st.session_state["cache"]["baggage_weight"],
)
st.session_state["cache"]["safety_margin"] = st.number_input(
    label="Safety Margin (%)",
    placeholder="30",
    key="safety_margin",
    value=st.session_state["cache"]["safety_margin"],
)
