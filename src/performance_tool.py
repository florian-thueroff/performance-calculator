from zipfile import ZipFile
from matplotlib import pyplot as plt
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
# from io import StringIO
import yaml
from yaml.loader import SafeLoader

if 'cache' not in st.session_state:
    metrics = [
        "airfield_name",
        "airfield_code",
        "airfield_elevation",
        "rw_heading",
        "aircraft_weight",
        "qnh",
        "oat",
        "wind_speed",
        "wind_direction",
    ]
    prefixes = [
        "alternate",
        "departure",
        "destination",
    ]
    for prefix in prefixes:
        for metric in metrics:
            st.session_state["cache"] = {f'{prefix}_{metric}': ""}

st.write("""
# Performance Tool
Enter your Flight information in the tabs
- general
- departure
- destination
- alternate

and download a printable performance and weight and balance summary in the "summary" tab.
""")

next_page = st.button(label="Get Started", type="primary")
if next_page:
    switch_page("general")

st.divider()

st.markdown("... or upload your configuration")
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = yaml.load(bytes_data, Loader=SafeLoader)
    st.session_state = data
    st.session_state["cache"] = data
    switch_page("summary")
