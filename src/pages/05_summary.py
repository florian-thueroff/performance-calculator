import tempfile
from zipfile import ZipFile
import streamlit as st
import matplotlib.pyplot as plt
import yaml

from my_html.renderer import HTMLRenderer, SummaryResultSet
from performance.plotter import plot_landingroll, plot_landingroll_over_15m_obstacle, plot_startroll, plot_startroll_over_15m_obstacle
from performance.solver import solve_landingroll_0m, solve_landingroll_15m, solve_startroll_0m, solve_startroll_15m
from utils.results_processor import PerformanceSet, calculate_perfromance

from weightbalance.plotter import plot_wb
from weightbalance.solver import solve_wb


if 'cache' not in st.session_state:
    st.session_state["cache"] = {}
metrics = [
    "airfield_name",
    "airfield_code",
    "airfield_elevation",
    "rw_heading",
    "fuel",
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
generals = [
    "departure_time",
    "arrival_time",
    "pilot_weight",
    "passenger_weight",
    "baggage_weight",
    "safety_margin",
]
for prefix in prefixes:
    for metric in metrics:
        key = f"{prefix}_{metric}"
        if key not in st.session_state["cache"]:
            if metric in ("airfield_name", "airfield_code"):
                st.session_state["cache"][key] = ""
            else:
                st.session_state["cache"][key] = 0
for key in generals:
    if key not in st.session_state["cache"]:
        if key in ("departure_time", "arrival_time"):
            st.session_state["cache"][key] = ""
        else:
            st.session_state["cache"][key] = 0


def _data_missing():
    metrics = [
        "airfield_name",
        "airfield_code",
        "airfield_elevation",
        "rw_heading",
        "fuel",
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
    generals = [
        "departure_time",
        "arrival_time",
        "pilot_weight",
        "passenger_weight",
        "baggage_weight",
        "safety_margin",
    ]
    for prefix in prefixes:
        for metric in metrics:
            key = f"{prefix}_{metric}"
            if key not in st.session_state["cache"]:
                return True
            elif metric in ("airfield_name", "airfield_code") and st.session_state["cache"][key] == "":
                return True
            elif metric == "qnh" and st.session_state["cache"][key] == 0:
                return True
    for key in generals:
        if key not in st.session_state["cache"]:
            return True
        elif key in ("departure_time", "arrival_time") and st.session_state["cache"][key] == "":
            return True
        elif metric == "pilot_weight" and st.session_state["cache"][key] == 0:
            return True
    return False

def data_missing(perf_set: PerformanceSet):
    return perf_set.departure_performance.perf_s0_data is None


st.set_page_config(page_title="Summary", page_icon="📈")
# st.markdown("# Summary")
st.sidebar.header("Summary")

with tempfile.TemporaryDirectory() as tmpdir:

    with st.spinner('Computing performance figures ...'):
        perf_set = calculate_perfromance(st.session_state, tmpdir)
    
    renderer = HTMLRenderer()
    if perf_set.departure_performance.wb_data is not None:
        renderer.add_wb("Departure", wb_res=perf_set.departure_performance.wb_data)
    if perf_set.destination_performance.wb_data is not None:
        renderer.add_wb("Destination", wb_res=perf_set.destination_performance.wb_data)
    if perf_set.alternate_performance.wb_data is not None:
        renderer.add_wb("Alternate", wb_res=perf_set.alternate_performance.wb_data)
    renderer.add_summary(
        alt=perf_set.alternate_performance.summary, 
        dep=perf_set.departure_performance.summary, 
        dest=perf_set.destination_performance.summary,
    )
    if perf_set.departure_performance.perf_s0_data is not None:
        renderer.add_perf(
            metric="Start Roll", 
            margin=st.session_state["cache"]["safety_margin"],
            res=perf_set.departure_performance.perf_s0_data,
        )
    if perf_set.departure_performance.perf_s15_data is not None:
        renderer.add_perf(
            metric="Start Roll Over 50ft Obstacle", 
            margin=st.session_state["cache"]["safety_margin"],
            res=perf_set.departure_performance.perf_s15_data,
        )
    if perf_set.destination_performance.perf_l0_data is not None:
        renderer.add_perf(
            metric="Landing Roll (Destination)", 
            margin=st.session_state["cache"]["safety_margin"],
            res=perf_set.destination_performance.perf_l0_data,
        )
    if perf_set.destination_performance.perf_l15_data is not None:
        renderer.add_perf(
            metric="Landing Roll Over 50ft Obstacle (Destination)", 
            margin=st.session_state["cache"]["safety_margin"],
            res=perf_set.destination_performance.perf_l15_data,
        )
    if perf_set.alternate_performance.perf_l0_data is not None:
        renderer.add_perf(
            metric="Landing Roll (Alternate)", 
            margin=st.session_state["cache"]["safety_margin"],
            res=perf_set.alternate_performance.perf_l0_data,
        )
    if perf_set.alternate_performance.perf_l15_data is not None:
        renderer.add_perf(
            metric="Landing Roll Over 50ft Obstacle (Alternate)", 
            margin=st.session_state["cache"]["safety_margin"],
            res=perf_set.alternate_performance.perf_l15_data,
        )

    with open(f"{tmpdir}/summary.html", "w") as f:
        html = renderer.render()
        f.write(html)

    with ZipFile(f"{tmpdir}/summary.zip", "w") as myzip:
        if perf_set.departure_performance.wb_fig is not None:
            myzip.write(f"{tmpdir}/wb_Departure.png")
        if perf_set.destination_performance.wb_fig is not None:
            myzip.write(f"{tmpdir}/wb_Destination.png")
        if perf_set.alternate_performance.wb_fig is not None:
            myzip.write(f"{tmpdir}/wb_Alternate.png")
        if perf_set.departure_performance.perf_s0_fig is not None:
            myzip.write(f"{tmpdir}/s0m_dep.png")
        if perf_set.departure_performance.perf_s15_fig is not None:
            myzip.write(f"{tmpdir}/s15m_dep.png")
        if perf_set.destination_performance.perf_l15_fig is not None:
            myzip.write(f"{tmpdir}/l15m_dest.png")
        if perf_set.destination_performance.perf_l0_fig is not None:
            myzip.write(f"{tmpdir}/l0m_dest.png")
        if perf_set.alternate_performance.perf_l15_fig is not None:
            myzip.write(f"{tmpdir}/l15m_alt.png")
        if perf_set.alternate_performance.perf_l0_fig is not None:
            myzip.write(f"{tmpdir}/l0m_alt.png")
        myzip.write(f"{tmpdir}/summary.html")
    
    with open(f"{tmpdir}/config.yaml", "w") as f:
        data = yaml.dump(st.session_state["cache"], f, sort_keys=False, default_flow_style=False)
    
    st.markdown("# Export")

    st.markdown("Export the current configuration")
    with open(f"{tmpdir}/config.yaml", "r") as fp:
        st.download_button(
            label="Save Configuration",
            data=fp,
            file_name="config.yaml",
            mime="text/yaml",
            disabled=data_missing(perf_set),
            type="secondary",
        )
    st.divider()
    st.markdown("Download a printable performance summary")
    with open(f"{tmpdir}/summary.zip", "rb") as fp:
        st.download_button(
            label="Download Summary",
            data=fp,
            file_name="summary.zip",
            mime="application/zip",
            disabled=data_missing(perf_set),
            type="primary",
        )
    
    st.markdown("# Summary")
    
    margin_factor = 1 + st.session_state["cache"]["safety_margin"] / 100.0

    if perf_set.departure_performance.perf_s0_data is not None:
        with st.expander(f"Start Roll @ {perf_set.departure_performance.summary.icao_code}"):
            base = perf_set.departure_performance.perf_s0_data.metric_value_bare
            corrected = perf_set.departure_performance.perf_s0_data.metric_value_corrected
            dcorrected = corrected - base
            final = margin_factor * corrected
            dfinal = final - base
            # st.markdown(f"## Start Roll @ {perf_set.departure_performance.summary.icao_code}")
            st.pyplot(perf_set.departure_performance.perf_s0_fig)
            st.divider()
            col1, col2, col3 = st.columns(3)
            col1.metric("Calm Winds", f"{round(base)} m")
            col2.metric("Forecast Wind", f"{round(corrected)} m", f"{round(dcorrected)} m", delta_color="inverse")
            col3.metric("Safe Value", f"{round(final)} m", f"{round(dfinal)} m", delta_color="inverse")
            st.divider()
    
    if perf_set.departure_performance.perf_s15_data is not None:
        with st.expander(f"Start Roll (15m Obstacle) @ {perf_set.departure_performance.summary.icao_code}"):
            base = perf_set.departure_performance.perf_s15_data.metric_value_bare
            corrected = perf_set.departure_performance.perf_s15_data.metric_value_corrected
            dcorrected = corrected - base
            final = margin_factor * corrected
            dfinal = final - base
            # st.markdown(f"## Start Roll (15m Obstacle) @ {perf_set.departure_performance.summary.icao_code}")
            st.pyplot(perf_set.departure_performance.perf_s15_fig)
            st.divider()
            col1, col2, col3 = st.columns(3)
            col1.metric("Calm Winds", f"{round(base)} m")
            col2.metric("Forecast Wind", f"{round(corrected)} m", f"{round(dcorrected)} m", delta_color="inverse")
            col3.metric("Safe Value", f"{round(final)} m", f"{round(dfinal)} m", delta_color="inverse")
            st.divider()
    
    if perf_set.destination_performance.perf_l0_data is not None:
        with st.expander(f"Landing Roll @ {perf_set.destination_performance.summary.icao_code}"):
            base = perf_set.destination_performance.perf_l0_data.metric_value_bare
            corrected = perf_set.destination_performance.perf_l0_data.metric_value_corrected
            dcorrected = corrected - base
            final = margin_factor * corrected
            dfinal = final - base
            # st.markdown(f"## Landing Roll @ {perf_set.destination_performance.summary.icao_code}")
            st.pyplot(perf_set.destination_performance.perf_l0_fig)
            st.divider()
            col1, col2, col3 = st.columns(3)
            col1.metric("Calm Winds", f"{round(base)} m")
            col2.metric("Forecast Wind", f"{round(corrected)} m", f"{round(dcorrected)} m", delta_color="inverse")
            col3.metric("Safe Value", f"{round(final)} m", f"{round(dfinal)} m", delta_color="inverse")
            st.divider()
    
    if perf_set.destination_performance.perf_l15_data is not None:
        with st.expander(f"Landing Roll (15m Obstacle) @ {perf_set.destination_performance.summary.icao_code}"):
            base = perf_set.destination_performance.perf_l15_data.metric_value_bare
            corrected = perf_set.destination_performance.perf_l15_data.metric_value_corrected
            dcorrected = corrected - base
            final = margin_factor * corrected
            dfinal = final - base
            # st.markdown(f"## Landing Roll (15m Obstacle) @ {perf_set.destination_performance.summary.icao_code}")
            st.pyplot(perf_set.destination_performance.perf_l15_fig)
            st.divider()
            col1, col2, col3 = st.columns(3)
            col1.metric("Calm Winds", f"{round(base)} m")
            col2.metric("Forecast Wind", f"{round(corrected)} m", f"{round(dcorrected)} m", delta_color="inverse")
            col3.metric("Safe Value", f"{round(final)} m", f"{round(dfinal)} m", delta_color="inverse")
            st.divider()
    
    if perf_set.alternate_performance.perf_l0_data is not None:
        with st.expander(f"Landing Roll @ {perf_set.alternate_performance.summary.icao_code}"):
            base = perf_set.alternate_performance.perf_l0_data.metric_value_bare
            corrected = perf_set.alternate_performance.perf_l0_data.metric_value_corrected
            dcorrected = corrected - base
            final = margin_factor * corrected
            dfinal = final - base
            # st.markdown(f"## Landing Roll @ {perf_set.alternate_performance.summary.icao_code}")
            st.pyplot(perf_set.alternate_performance.perf_l0_fig)
            st.divider()
            col1, col2, col3 = st.columns(3)
            col1.metric("Calm Winds", f"{round(base)} m")
            col2.metric("Forecast Wind", f"{round(corrected)} m", f"{round(dcorrected)} m", delta_color="inverse")
            col3.metric("Safe Value", f"{round(final)} m", f"{round(dfinal)} m", delta_color="inverse")
            st.divider()
    
    if perf_set.alternate_performance.perf_l15_data is not None:
        with st.expander(f"Landing Roll (15m Obstacle) @ {perf_set.alternate_performance.summary.icao_code}"):
            base = perf_set.alternate_performance.perf_l15_data.metric_value_bare
            corrected = perf_set.alternate_performance.perf_l15_data.metric_value_corrected
            dcorrected = corrected - base
            final = margin_factor * corrected
            dfinal = final - base
            # st.markdown(f"## Landing Roll (15m Obstacle) @ {perf_set.alternate_performance.summary.icao_code}")
            st.pyplot(perf_set.alternate_performance.perf_l15_fig)
            st.divider()
            col1, col2, col3 = st.columns(3)
            col1.metric("Calm Winds", f"{round(base)} m")
            col2.metric("Forecast Wind", f"{round(corrected)} m", f"{round(dcorrected)} m", delta_color="inverse")
            col3.metric("Safe Value", f"{round(final)} m", f"{round(dfinal)} m", delta_color="inverse")
            st.divider()
    
    if perf_set.departure_performance.wb_data is not None:
        with st.expander(f"Weight & Balance @ {perf_set.departure_performance.summary.icao_code}"):
            weight = perf_set.departure_performance.wb_data.weight_total
            dweight = 780 - weight
            torque = perf_set.departure_performance.wb_data.momentum_total
            torque_label = "OK" if perf_set.departure_performance.wb_data.within_limits else "-NOT OK-"
            # st.markdown(f"## Weight & Balance @ {perf_set.departure_performance.summary.icao_code}")
            st.pyplot(perf_set.departure_performance.wb_fig)
            st.divider()
            col1, col2 = st.columns(2)
            col1.metric("Weight", f"{round(weight)} kg", f"{round(dweight)} kg")
            col2.metric("Torque", f"{round(torque)} kgm", torque_label)
            st.divider()
    
    if perf_set.destination_performance.wb_data is not None:
        with st.expander(f"Weight & Balance @ {perf_set.destination_performance.summary.icao_code}"):
            weight = perf_set.destination_performance.wb_data.weight_total
            dweight = 780 - weight
            torque = perf_set.destination_performance.wb_data.momentum_total
            torque_label = "OK" if perf_set.destination_performance.wb_data.within_limits else "-NOT OK-"
            # st.markdown(f"## Weight & Balance @ {perf_set.destination_performance.summary.icao_code}")
            st.pyplot(perf_set.destination_performance.wb_fig)
            st.divider()
            col1, col2 = st.columns(2)
            col1.metric("Weight", f"{round(weight)} kg", f"{round(dweight)} kg")
            col2.metric("Torque", f"{round(torque)} kgm", torque_label)
            st.divider()
    
    if perf_set.alternate_performance.wb_data is not None:
        with st.expander(f"Weight & Balance @ {perf_set.alternate_performance.summary.icao_code}"):
            weight = perf_set.alternate_performance.wb_data.weight_total
            dweight = 780 - weight
            torque = perf_set.alternate_performance.wb_data.momentum_total
            torque_label = "OK" if perf_set.alternate_performance.wb_data.within_limits else "-NOT OK-"
            # st.markdown(f"## Weight & Balance @ {perf_set.alternate_performance.summary.icao_code}")
            st.pyplot(perf_set.alternate_performance.wb_fig)
            st.divider()
            col1, col2 = st.columns(2)
            col1.metric("Weight", f"{round(weight)} kg", f"{round(dweight)} kg")
            col2.metric("Torque", f"{round(torque)} kgm", torque_label)
            st.divider()
