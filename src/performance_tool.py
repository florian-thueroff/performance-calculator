from zipfile import ZipFile
from matplotlib import pyplot as plt
import streamlit as st
import tempfile

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
