from dataclasses import dataclass, field
from typing import Optional

from matplotlib.figure import Figure
from my_html.renderer import SummaryResultSet
from performance.plotter import plot_landingroll, plot_landingroll_over_15m_obstacle, plot_startroll, plot_startroll_over_15m_obstacle
from performance.solver import PerformanceResultSet, solve_landingroll_0m, solve_landingroll_15m, solve_startroll_0m, solve_startroll_15m
from weightbalance.plotter import plot_wb
from weightbalance.solver import WBResultSet, solve_wb


@dataclass 
class TakeoffPerformance:
    wb_data: Optional[WBResultSet] = field(default=None)
    wb_fig: Optional[Figure] = field(default=None)
    perf_s0_data: Optional[PerformanceResultSet] = field(default=None)
    perf_s0_fig: Optional[Figure] = field(default=None)
    perf_s15_data: Optional[PerformanceResultSet] = field(default=None)
    perf_s15_fig: Optional[Figure] = field(default=None)
    summary: Optional[SummaryResultSet] = field(default=None)


@dataclass 
class LandingPerformance:
    wb_data: Optional[WBResultSet] = field(default=None)
    wb_fig: Optional[Figure] = field(default=None)
    perf_l0_data: Optional[PerformanceResultSet] = field(default=None)
    perf_l0_fig: Optional[Figure] = field(default=None)
    perf_l15_data: Optional[PerformanceResultSet] = field(default=None)
    perf_l15_fig: Optional[Figure] = field(default=None)
    summary: Optional[SummaryResultSet] = field(default=None)


@dataclass
class PerformanceSet:
    departure_performance: TakeoffPerformance
    destination_performance: LandingPerformance
    alternate_performance: LandingPerformance


def _keys_in(object, some=[], any=[], debug=False):
    checksum = 0
    if debug: print(f"inspecting: {object}")
    for key in some:
        if key not in object:
            if debug: print(f"key '{key}' is not in object!")
            return False
        if object[key] != 0 and object[key] != "":
            checksum += 1
    for key in any:
        checksum += 1
        if key not in object:
            if debug: print(f"key '{key}' is not in object!")
            return False
        if object[key] == 0 or object[key] == "" or object[key] is None:
            if debug: print(f"key '{key}' is not set!")
            return False
    if debug: print(f"returning checksum = {checksum}")
    return checksum > 0


def calculate_perfromance(session_state, tmpdir) -> PerformanceSet:

    wb_res_dep = None
    fig_dep_wb = None
    wb_res_dest = None
    fig_dest_wb = None
    wb_res_alt = None
    fig_alt_wb = None
    perf_dep_s0m = None
    perf_dep_s15m = None
    fig_dep_s0 = None
    fig_dep_s15 = None
    perf_dest_l0m = None
    perf_dest_l15m = None
    fig_dest_l0 = None
    fig_dest_l15 = None
    perf_alt_l0m = None
    perf_alt_l15m = None
    fig_alt_l0 = None
    fig_alt_l15 = None
    sum_dep = None
    sum_dest = None
    sum_alt = None
    
    keys_wb = ("baggage_weight", "pilot_weight", "passenger_weight")
    keys_perf_dep = ("departure_airfield_elevation", "departure_qnh", "departure_rw_heading", "departure_oat", "departure_wind_direction", "departure_wind_speed")
    keys_perf_dest = ("destination_airfield_elevation", "destination_qnh", "destination_rw_heading", "destination_oat", "destination_wind_direction", "destination_wind_speed")
    keys_perf_alt = ("alternate_airfield_elevation", "alternate_qnh", "alternate_rw_heading", "alternate_oat", "alternate_wind_direction", "alternate_wind_speed")

    if _keys_in(some=keys_wb, any=tuple(["departure_fuel"]), object=session_state["cache"]):
        wb_res_dep = solve_wb(
            baggage_weight_kg=session_state["cache"]["baggage_weight"],
            pilot_weight_kg=session_state["cache"]["pilot_weight"],
            passenger_weight_kg=session_state["cache"]["passenger_weight"],
            fuel_litres=session_state["cache"]["departure_fuel"],
            empty_moment_kgm=167.88,
            empty_weight_kg=556.5
        )
        fig_dep_wb = plot_wb(
            baggage_weight_kg=session_state["cache"]["baggage_weight"],
            pilot_weight_kg=session_state["cache"]["pilot_weight"],
            passenger_weight_kg=session_state["cache"]["passenger_weight"],
            fuel_litres=session_state["cache"]["departure_fuel"],
            empty_moment_kgm=167.88,
            empty_weight_kg=556.5,
            folder=tmpdir,
            filename="wb_Departure"
        )
    
    if _keys_in(some=keys_wb, any=tuple(["destination_fuel"]), object=session_state["cache"]):
        wb_res_dest = solve_wb(
            baggage_weight_kg=session_state["cache"]["baggage_weight"],
            pilot_weight_kg=session_state["cache"]["pilot_weight"],
            passenger_weight_kg=session_state["cache"]["passenger_weight"],
            fuel_litres=session_state["cache"]["destination_fuel"],
            empty_moment_kgm=167.88,
            empty_weight_kg=556.5
        )
        fig_dest_wb = plot_wb(
            baggage_weight_kg=session_state["cache"]["baggage_weight"],
            pilot_weight_kg=session_state["cache"]["pilot_weight"],
            passenger_weight_kg=session_state["cache"]["passenger_weight"],
            fuel_litres=session_state["cache"]["destination_fuel"],
            empty_moment_kgm=167.88,
            empty_weight_kg=556.5,
            folder=tmpdir,
            filename="wb_Destination"
        )
    
    if _keys_in(some=keys_wb, any=tuple(["alternate_fuel"]), object=session_state["cache"]):
        wb_res_alt = solve_wb(
            baggage_weight_kg=session_state["cache"]["baggage_weight"],
            pilot_weight_kg=session_state["cache"]["pilot_weight"],
            passenger_weight_kg=session_state["cache"]["passenger_weight"],
            fuel_litres=session_state["cache"]["alternate_fuel"],
            empty_moment_kgm=167.88,
            empty_weight_kg=556.5
        )
        fig_alt_wb = plot_wb(
            baggage_weight_kg=session_state["cache"]["baggage_weight"],
            pilot_weight_kg=session_state["cache"]["pilot_weight"],
            passenger_weight_kg=session_state["cache"]["passenger_weight"],
            fuel_litres=session_state["cache"]["alternate_fuel"],
            empty_moment_kgm=167.88,
            empty_weight_kg=556.5,
            folder=tmpdir,
            filename="wb_Alternate"
        )

    if _keys_in(some=keys_perf_dep, object=session_state["cache"]) and wb_res_dep is not None:
        perf_dep_s0m = solve_startroll_0m(
            alt=session_state["cache"]["departure_airfield_elevation"],
            is_grass=False,
            qnh=session_state["cache"]["departure_qnh"],
            rw_heading=session_state["cache"]["departure_rw_heading"],
            temp=session_state["cache"]["departure_oat"],
            weight=wb_res_dep.weight_total,
            wind_direction=session_state["cache"]["departure_wind_direction"],
            wind_speed=session_state["cache"]["departure_wind_speed"],
        )
        fig_dep_s0 = plot_startroll(
            weight=wb_res_dep.weight_total, 
            temp=perf_dep_s0m.oat, 
            alt=session_state["cache"]["departure_airfield_elevation"],
            qnh=perf_dep_s0m.qnh,
            folder=tmpdir,
            file="s0m_dep"
        )
        perf_dep_s15m = solve_startroll_15m(
            alt=session_state["cache"]["departure_airfield_elevation"],
            is_grass=False,
            qnh=session_state["cache"]["departure_qnh"],
            rw_heading=session_state["cache"]["departure_rw_heading"],
            temp=session_state["cache"]["departure_oat"],
            weight=wb_res_dep.weight_total,
            wind_direction=session_state["cache"]["departure_wind_direction"],
            wind_speed=session_state["cache"]["departure_wind_speed"],
        )
        fig_dep_s15 = plot_startroll_over_15m_obstacle(
            weight=wb_res_dep.weight_total, 
            temp=perf_dep_s0m.oat, 
            alt=session_state["cache"]["departure_airfield_elevation"],
            qnh=perf_dep_s0m.qnh,
            folder=tmpdir,
            file="s15m_dep",
        )
    
    if _keys_in(some=keys_perf_dest, object=session_state["cache"]) and wb_res_dest is not None:
        perf_dest_l0m = solve_landingroll_0m(
            alt=session_state["cache"]["destination_airfield_elevation"],
            is_grass=False,
            qnh=session_state["cache"]["destination_qnh"],
            rw_heading=session_state["cache"]["destination_rw_heading"],
            temp=session_state["cache"]["destination_oat"],
            weight=wb_res_dest.weight_total,
            wind_direction=session_state["cache"]["destination_wind_direction"],
            wind_speed=session_state["cache"]["destination_wind_speed"],
        )
        fig_dest_l0 = plot_landingroll(
            weight=wb_res_dest.weight_total, 
            temp=perf_dest_l0m.oat, 
            alt=session_state["cache"]["destination_airfield_elevation"],
            qnh=perf_dest_l0m.qnh,
            folder=tmpdir,
            file="l0m_dest",
        )
        perf_dest_l15m = solve_landingroll_15m(
            alt=session_state["cache"]["destination_airfield_elevation"],
            is_grass=False,
            qnh=session_state["cache"]["destination_qnh"],
            rw_heading=session_state["cache"]["destination_rw_heading"],
            temp=session_state["cache"]["destination_oat"],
            weight=wb_res_dest.weight_total,
            wind_direction=session_state["cache"]["destination_wind_direction"],
            wind_speed=session_state["cache"]["destination_wind_speed"],
        )
        fig_dest_l15 = plot_landingroll_over_15m_obstacle(
            weight=wb_res_dest.weight_total, 
            temp=perf_dest_l0m.oat, 
            alt=session_state["cache"]["destination_airfield_elevation"],
            qnh=perf_dest_l0m.qnh,
            folder=tmpdir,
            file="l15m_dest",
        )
    elif _keys_in(some=keys_perf_dep, object=session_state["cache"]) and wb_res_dep is not None:
        perf_dest_l0m = solve_landingroll_0m(
            alt=session_state["cache"]["departure_airfield_elevation"],
            is_grass=False,
            qnh=session_state["cache"]["departure_qnh"],
            rw_heading=session_state["cache"]["departure_rw_heading"],
            temp=session_state["cache"]["departure_oat"],
            weight=wb_res_dep.weight_total,
            wind_direction=session_state["cache"]["departure_wind_direction"],
            wind_speed=session_state["cache"]["departure_wind_speed"],
        )
        fig_dest_l0 = plot_landingroll(
            weight=wb_res_dep.weight_total, 
            temp=perf_dest_l0m.oat, 
            alt=session_state["cache"]["departure_airfield_elevation"],
            qnh=perf_dest_l0m.qnh,
            folder=tmpdir,
            file="l0m_dest",
        )
        perf_dest_l15m = solve_landingroll_15m(
            alt=session_state["cache"]["departure_airfield_elevation"],
            is_grass=False,
            qnh=session_state["cache"]["departure_qnh"],
            rw_heading=session_state["cache"]["departure_rw_heading"],
            temp=session_state["cache"]["departure_oat"],
            weight=wb_res_dep.weight_total,
            wind_direction=session_state["cache"]["departure_wind_direction"],
            wind_speed=session_state["cache"]["departure_wind_speed"],
        )
        fig_dest_l15 = plot_landingroll_over_15m_obstacle(
            weight=wb_res_dep.weight_total, 
            temp=perf_dest_l0m.oat, 
            alt=session_state["cache"]["departure_airfield_elevation"],
            qnh=perf_dest_l0m.qnh,
            folder=tmpdir,
            file="l15m_dest",
        )

    if _keys_in(some=keys_perf_alt, object=session_state["cache"]) and wb_res_alt is not None:
        perf_alt_l0m = solve_landingroll_0m(
            alt=session_state["cache"]["alternate_airfield_elevation"],
            is_grass=False,
            qnh=session_state["cache"]["alternate_qnh"],
            rw_heading=session_state["cache"]["alternate_rw_heading"],
            temp=session_state["cache"]["alternate_oat"],
            weight=wb_res_alt.weight_total,
            wind_direction=session_state["cache"]["alternate_wind_direction"],
            wind_speed=session_state["cache"]["alternate_wind_speed"],
        )
        fig_alt_l0 = plot_landingroll(
            weight=wb_res_alt.weight_total, 
            temp=perf_alt_l0m.oat, 
            alt=session_state["cache"]["alternate_airfield_elevation"],
            qnh=perf_alt_l0m.qnh,
            folder=tmpdir,
            file="l0m_alt",
        )
        perf_alt_l15m = solve_landingroll_15m(
            alt=session_state["cache"]["alternate_airfield_elevation"],
            is_grass=False,
            qnh=session_state["cache"]["alternate_qnh"],
            rw_heading=session_state["cache"]["alternate_rw_heading"],
            temp=session_state["cache"]["alternate_oat"],
            weight=wb_res_alt.weight_total,
            wind_direction=session_state["cache"]["alternate_wind_direction"],
            wind_speed=session_state["cache"]["alternate_wind_speed"],
        )
        fig_alt_l15 = plot_landingroll_over_15m_obstacle(
            weight=wb_res_alt.weight_total, 
            temp=perf_alt_l0m.oat, 
            alt=session_state["cache"]["alternate_airfield_elevation"],
            qnh=perf_alt_l0m.qnh,
            folder=tmpdir,
            file="l15m_alt",
        )
    
    if _keys_in(some=("departure_airfield_elevation", "departure_airfield_code", "departure_time"), object=session_state["cache"]) and perf_dep_s0m is not None:
        sum_dep = SummaryResultSet(
            elevation=session_state["cache"]["departure_airfield_elevation"],
            headwind_component=perf_dep_s0m.headwind_component,
            icao_code=session_state["cache"]["departure_airfield_code"],
            oat=perf_dep_s0m.oat,
            pressure_altitude=perf_dep_s0m.pressure_altitude,
            qnh=perf_dep_s0m.qnh,
            rw_heading=perf_dep_s0m.rw_heading,
            time=session_state["cache"]["departure_time"],
            wind_direction=perf_dep_s0m.wind_direction,
            wind_speed=perf_dep_s0m.wind_speed,
        )

    if _keys_in(any=("destination_airfield_elevation", "destination_airfield_code", "arrival_time"), object=session_state["cache"]) and perf_dest_l0m is not None:
        sum_dest = SummaryResultSet(
            elevation=session_state["cache"]["destination_airfield_elevation"],
            headwind_component=perf_dest_l0m.headwind_component,
            icao_code=session_state["cache"]["destination_airfield_code"],
            oat=perf_dest_l0m.oat,
            pressure_altitude=perf_dest_l0m.pressure_altitude,
            qnh=perf_dest_l0m.qnh,
            rw_heading=perf_dest_l0m.rw_heading,
            time=session_state["cache"]["arrival_time"],
            wind_direction=perf_dest_l0m.wind_direction,
            wind_speed=perf_dest_l0m.wind_speed,
        )
    elif _keys_in(some=("departure_airfield_elevation", "departure_airfield_code", "arrival_time"), object=session_state["cache"]) and perf_dest_l0m is not None:
        sum_dest = SummaryResultSet(
            elevation=session_state["cache"]["departure_airfield_elevation"],
            headwind_component=perf_dest_l0m.headwind_component,
            icao_code=session_state["cache"]["departure_airfield_code"],
            oat=perf_dest_l0m.oat,
            pressure_altitude=perf_dest_l0m.pressure_altitude,
            qnh=perf_dest_l0m.qnh,
            rw_heading=perf_dest_l0m.rw_heading,
            time=session_state["cache"]["arrival_time"],
            wind_direction=perf_dest_l0m.wind_direction,
            wind_speed=perf_dest_l0m.wind_speed,
        )
    
    if _keys_in(some=("alternate_airfield_elevation", "alternate_airfield_code"), object=session_state["cache"]) and perf_alt_l0m is not None:
        sum_alt = SummaryResultSet(
            elevation=session_state["cache"]["alternate_airfield_elevation"],
            headwind_component=perf_alt_l0m.headwind_component,
            icao_code=session_state["cache"]["alternate_airfield_code"],
            oat=perf_alt_l0m.oat,
            pressure_altitude=perf_alt_l0m.pressure_altitude,
            qnh=perf_alt_l0m.qnh,
            rw_heading=perf_alt_l0m.rw_heading,
            time="",
            wind_direction=perf_alt_l0m.wind_direction,
            wind_speed=perf_alt_l0m.wind_speed,
        )
    
    return PerformanceSet(
        departure_performance=TakeoffPerformance(
            perf_s0_data=perf_dep_s0m,
            perf_s15_data=perf_dep_s15m,
            perf_s0_fig=fig_dep_s0,
            perf_s15_fig=fig_dep_s15,
            wb_data=wb_res_dep,
            wb_fig=fig_dep_wb,
            summary=sum_dep,
        ),
        destination_performance=LandingPerformance(
            perf_l0_data=perf_dest_l0m,
            perf_l15_data=perf_dest_l15m,
            perf_l0_fig=fig_dest_l0,
            perf_l15_fig=fig_dest_l15,
            wb_data=wb_res_dest,
            wb_fig=fig_dest_wb,
            summary=sum_dest,
        ),
        alternate_performance=LandingPerformance(
            perf_l0_data=perf_alt_l0m,
            perf_l15_data=perf_alt_l15m,
            perf_l0_fig=fig_alt_l0,
            perf_l15_fig=fig_alt_l15,
            wb_data=wb_res_alt,
            wb_fig=fig_alt_wb,
            summary=sum_alt,
        ),
    )
