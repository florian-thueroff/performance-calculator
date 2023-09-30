import tempfile
from zipfile import ZipFile
import streamlit as st
from my_html.renderer import HTMLRenderer, SummaryResultSet
from performance.plotter import plot_landingroll, plot_landingroll_over_15m_obstacle, plot_startroll, plot_startroll_over_15m_obstacle
from performance.solver import solve_landingroll_0m, solve_landingroll_15m, solve_startroll_0m, solve_startroll_15m

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


def data_missing():
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


st.set_page_config(page_title="Summary", page_icon="📈")
st.markdown("# Summary")
st.sidebar.header("Summary")
st.write(
    """Wait a second for the download button to appear, which allows you to download a printable weight and balance and performance summary for your planned flight."""
)

# st.write(st.session_state)


with tempfile.TemporaryDirectory() as tmpdir:
    renderer = HTMLRenderer()
    wb_res_dep = solve_wb(
        baggage_weight_kg=st.session_state["cache"]["baggage_weight"],
        pilot_weight_kg=st.session_state["cache"]["pilot_weight"],
        passenger_weight_kg=st.session_state["cache"]["passenger_weight"],
        fuel_litres=st.session_state["cache"]["departure_fuel"],
        empty_moment_kgm=167.88,
        empty_weight_kg=556.5
    )
    wb_res_dest = solve_wb(
        baggage_weight_kg=st.session_state["cache"]["baggage_weight"],
        pilot_weight_kg=st.session_state["cache"]["pilot_weight"],
        passenger_weight_kg=st.session_state["cache"]["passenger_weight"],
        fuel_litres=st.session_state["cache"]["destination_fuel"],
        empty_moment_kgm=167.88,
        empty_weight_kg=556.5
    )
    wb_res_alt = solve_wb(
        baggage_weight_kg=st.session_state["cache"]["baggage_weight"],
        pilot_weight_kg=st.session_state["cache"]["pilot_weight"],
        passenger_weight_kg=st.session_state["cache"]["passenger_weight"],
        fuel_litres=st.session_state["cache"]["alternate_fuel"],
        empty_moment_kgm=167.88,
        empty_weight_kg=556.5
    )
    renderer.add_wb("Departure", wb_res=wb_res_dep)
    renderer.add_wb("Destination", wb_res=wb_res_dest)
    renderer.add_wb("Alternate", wb_res=wb_res_alt)

    perf_dep_s0m = solve_startroll_0m(
        alt=st.session_state["cache"]["departure_airfield_elevation"],
        is_grass=False,
        qnh=st.session_state["cache"]["departure_qnh"],
        rw_heading=st.session_state["cache"]["departure_rw_heading"],
        temp=st.session_state["cache"]["departure_oat"],
        weight=wb_res_dep.weight_total,
        wind_direction=st.session_state["cache"]["departure_wind_direction"],
        wind_speed=st.session_state["cache"]["departure_wind_speed"],
    )
    perf_dep_s15m = solve_startroll_15m(
        alt=st.session_state["cache"]["departure_airfield_elevation"],
        is_grass=False,
        qnh=st.session_state["cache"]["departure_qnh"],
        rw_heading=st.session_state["cache"]["departure_rw_heading"],
        temp=st.session_state["cache"]["departure_oat"],
        weight=wb_res_dep.weight_total,
        wind_direction=st.session_state["cache"]["departure_wind_direction"],
        wind_speed=st.session_state["cache"]["departure_wind_speed"],
    )
    perf_dest_s0m = solve_startroll_0m(
        alt=st.session_state["cache"]["destination_airfield_elevation"],
        is_grass=False,
        qnh=st.session_state["cache"]["destination_qnh"],
        rw_heading=st.session_state["cache"]["destination_rw_heading"],
        temp=st.session_state["cache"]["destination_oat"],
        weight=wb_res_dest.weight_total,
        wind_direction=st.session_state["cache"]["destination_wind_direction"],
        wind_speed=st.session_state["cache"]["destination_wind_speed"],
    )
    perf_dest_l0m = solve_landingroll_0m(
        alt=st.session_state["cache"]["destination_airfield_elevation"],
        is_grass=False,
        qnh=st.session_state["cache"]["destination_qnh"],
        rw_heading=st.session_state["cache"]["destination_rw_heading"],
        temp=st.session_state["cache"]["destination_oat"],
        weight=wb_res_dest.weight_total,
        wind_direction=st.session_state["cache"]["destination_wind_direction"],
        wind_speed=st.session_state["cache"]["destination_wind_speed"],
    )
    perf_dest_l15m = solve_landingroll_15m(
        alt=st.session_state["cache"]["destination_airfield_elevation"],
        is_grass=False,
        qnh=st.session_state["cache"]["destination_qnh"],
        rw_heading=st.session_state["cache"]["destination_rw_heading"],
        temp=st.session_state["cache"]["destination_oat"],
        weight=wb_res_dest.weight_total,
        wind_direction=st.session_state["cache"]["destination_wind_direction"],
        wind_speed=st.session_state["cache"]["destination_wind_speed"],
    )
    perf_alt_s0m = solve_startroll_0m(
        alt=st.session_state["cache"]["alternate_airfield_elevation"],
        is_grass=False,
        qnh=st.session_state["cache"]["alternate_qnh"],
        rw_heading=st.session_state["cache"]["alternate_rw_heading"],
        temp=st.session_state["cache"]["alternate_oat"],
        weight=wb_res_alt.weight_total,
        wind_direction=st.session_state["cache"]["alternate_wind_direction"],
        wind_speed=st.session_state["cache"]["alternate_wind_speed"],
    )
    perf_alt_l0m = solve_landingroll_0m(
        alt=st.session_state["cache"]["alternate_airfield_elevation"],
        is_grass=False,
        qnh=st.session_state["cache"]["alternate_qnh"],
        rw_heading=st.session_state["cache"]["alternate_rw_heading"],
        temp=st.session_state["cache"]["alternate_oat"],
        weight=wb_res_alt.weight_total,
        wind_direction=st.session_state["cache"]["alternate_wind_direction"],
        wind_speed=st.session_state["cache"]["alternate_wind_speed"],
    )
    perf_alt_l15m = solve_landingroll_15m(
        alt=st.session_state["cache"]["alternate_airfield_elevation"],
        is_grass=False,
        qnh=st.session_state["cache"]["alternate_qnh"],
        rw_heading=st.session_state["cache"]["alternate_rw_heading"],
        temp=st.session_state["cache"]["alternate_oat"],
        weight=wb_res_alt.weight_total,
        wind_direction=st.session_state["cache"]["alternate_wind_direction"],
        wind_speed=st.session_state["cache"]["alternate_wind_speed"],
    )
    sum_dep = SummaryResultSet(
        elevation=st.session_state["cache"]["departure_airfield_elevation"],
        headwind_component=perf_dep_s0m.headwind_component,
        icao_code=st.session_state["cache"]["departure_airfield_code"],
        oat=perf_dep_s0m.oat,
        pressure_altitude=perf_dep_s0m.pressure_altitude,
        qnh=perf_dep_s0m.qnh,
        rw_heading=perf_dep_s0m.rw_heading,
        time=st.session_state["cache"]["departure_time"],
        wind_direction=perf_dep_s0m.wind_direction,
        wind_speed=perf_dep_s0m.wind_speed,
    )
    sum_dest = SummaryResultSet(
        elevation=st.session_state["cache"]["destination_airfield_elevation"],
        headwind_component=perf_dest_s0m.headwind_component,
        icao_code=st.session_state["cache"]["destination_airfield_code"],
        oat=perf_dest_s0m.oat,
        pressure_altitude=perf_dest_s0m.pressure_altitude,
        qnh=perf_dest_s0m.qnh,
        rw_heading=perf_dest_s0m.rw_heading,
        time=st.session_state["cache"]["arrival_time"],
        wind_direction=perf_dest_s0m.wind_direction,
        wind_speed=perf_dest_s0m.wind_speed,
    )
    sum_alt = SummaryResultSet(
        elevation=st.session_state["cache"]["alternate_airfield_elevation"],
        headwind_component=perf_alt_s0m.headwind_component,
        icao_code=st.session_state["cache"]["alternate_airfield_code"],
        oat=perf_alt_s0m.oat,
        pressure_altitude=perf_alt_s0m.pressure_altitude,
        qnh=perf_alt_s0m.qnh,
        rw_heading=perf_alt_s0m.rw_heading,
        time="",
        wind_direction=perf_alt_s0m.wind_direction,
        wind_speed=perf_alt_s0m.wind_speed,
    )
    renderer.add_summary(alt=sum_alt, dep=sum_dep, dest=sum_dest)
    renderer.add_perf(
        metric="Start Roll", 
        margin=st.session_state["cache"]["safety_margin"],
        res=perf_dep_s0m,
    )
    renderer.add_perf(
        metric="Start Roll Over 50ft Obstacle", 
        margin=st.session_state["cache"]["safety_margin"],
        res=perf_dep_s15m,
    )
    renderer.add_perf(
        metric="Landing Roll (Destination)", 
        margin=st.session_state["cache"]["safety_margin"],
        res=perf_dest_l0m,
    )
    renderer.add_perf(
        metric="Landing Roll Over 50ft Obstacle (Destination)", 
        margin=st.session_state["cache"]["safety_margin"],
        res=perf_dest_l15m,
    )
    renderer.add_perf(
        metric="Landing Roll (Alternate)", 
        margin=st.session_state["cache"]["safety_margin"],
        res=perf_alt_l0m,
    )
    renderer.add_perf(
        metric="Landing Roll Over 50ft Obstacle (Alternate)", 
        margin=st.session_state["cache"]["safety_margin"],
        res=perf_alt_l15m,
    )

    with open(f"{tmpdir}/summary.html", "w") as f:
        html = renderer.render()
        f.write(html)
    
    plot_wb(
        baggage_weight_kg=st.session_state["cache"]["baggage_weight"],
        pilot_weight_kg=st.session_state["cache"]["pilot_weight"],
        passenger_weight_kg=st.session_state["cache"]["passenger_weight"],
        fuel_litres=st.session_state["cache"]["departure_fuel"],
        empty_moment_kgm=167.88,
        empty_weight_kg=556.5,
        folder=tmpdir,
        filename="wb_Departure"
    )
    plot_wb(
        baggage_weight_kg=st.session_state["cache"]["baggage_weight"],
        pilot_weight_kg=st.session_state["cache"]["pilot_weight"],
        passenger_weight_kg=st.session_state["cache"]["passenger_weight"],
        fuel_litres=st.session_state["cache"]["destination_fuel"],
        empty_moment_kgm=167.88,
        empty_weight_kg=556.5,
        folder=tmpdir,
        filename="wb_Destination"
    )
    plot_wb(
        baggage_weight_kg=st.session_state["cache"]["baggage_weight"],
        pilot_weight_kg=st.session_state["cache"]["pilot_weight"],
        passenger_weight_kg=st.session_state["cache"]["passenger_weight"],
        fuel_litres=st.session_state["cache"]["alternate_fuel"],
        empty_moment_kgm=167.88,
        empty_weight_kg=556.5,
        folder=tmpdir,
        filename="wb_Alternate"
    )
    plot_startroll(
        weight=wb_res_dep.weight_total, 
        temp=perf_dep_s0m.oat, 
        alt=st.session_state["cache"]["departure_airfield_elevation"],
        qnh=perf_dep_s0m.qnh,
        folder=tmpdir,
        file="s0m_dep"
    )

    plot_startroll_over_15m_obstacle(
        weight=wb_res_dep.weight_total, 
        temp=perf_dep_s0m.oat, 
        alt=st.session_state["cache"]["departure_airfield_elevation"],
        qnh=perf_dep_s0m.qnh,
        folder=tmpdir,
        file="s15m_dep",
    )

    plot_landingroll_over_15m_obstacle(
        weight=wb_res_dest.weight_total, 
        temp=perf_dest_s0m.oat, 
        alt=st.session_state["cache"]["destination_airfield_elevation"],
        qnh=perf_dest_s0m.qnh,
        folder=tmpdir,
        file="l15m_dest",
    )

    plot_landingroll_over_15m_obstacle(
        weight=wb_res_alt.weight_total, 
        temp=perf_alt_s0m.oat, 
        alt=st.session_state["cache"]["alternate_airfield_elevation"],
        qnh=perf_alt_s0m.qnh,
        folder=tmpdir,
        file="l15m_alt",
    )

    plot_landingroll(
        weight=wb_res_dest.weight_total, 
        temp=perf_dest_s0m.oat, 
        alt=st.session_state["cache"]["destination_airfield_elevation"],
        qnh=perf_dest_s0m.qnh,
        folder=tmpdir,
        file="l0m_dest",
    )

    plot_landingroll(
        weight=wb_res_alt.weight_total, 
        temp=perf_alt_s0m.oat, 
        alt=st.session_state["cache"]["alternate_airfield_elevation"],
        qnh=perf_alt_s0m.qnh,
        folder=tmpdir,
        file="l0m_alt",
    )

    with ZipFile(f"{tmpdir}/summary.zip", "w") as myzip:
        myzip.write(f"{tmpdir}/wb_Departure.png")
        myzip.write(f"{tmpdir}/wb_Destination.png")
        myzip.write(f"{tmpdir}/wb_Alternate.png")
        myzip.write(f"{tmpdir}/s0m_dep.png")
        myzip.write(f"{tmpdir}/s15m_dep.png")
        myzip.write(f"{tmpdir}/l15m_dest.png")
        myzip.write(f"{tmpdir}/l0m_dest.png")
        myzip.write(f"{tmpdir}/l15m_alt.png")
        myzip.write(f"{tmpdir}/l0m_alt.png")
        myzip.write(f"{tmpdir}/summary.html")
    
    with open(f"{tmpdir}/summary.zip", "rb") as fp:
        st.download_button(
            label="Download Summary",
            data=fp,
            file_name="summary.zip",
            mime="application/zip",
            disabled=data_missing()
        )