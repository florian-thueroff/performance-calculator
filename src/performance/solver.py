from dataclasses import dataclass, field
import math

from model.first_order_polynomial import FirstOrderPolynomial
from model.first_order_rational import FirstOrderRational
from model.second_order_polynomial import SecondOrderPolynomial
from model.second_order_rational import SecondOrderRational
from performance.models import get_model_branches
from utils.converter import elevation2pressurealtitude

## CALIBRATION RIGHT BRANCH (from graph in operatng manual)
config_to_dist = {
    "FIT_UPPER_RIGHT": [[600, 230], [700, 334], [780, 432]],  # upper right branch
    "FIT_MID_RIGHT": [[600, 170], [720, 260], [776, 310]],  # mid right branch
    "FIT_LOWER_RIGHT": [[604, 130], [684, 170], [780, 230]],  # lower right branch
    "FIT_UPPER_LEFT": [[-14, 209], [48, 321]],  # upper left branch
    "FIT_MID_LEFT": [[-14, 149.5], [40, 210]],  # mid left branch
    "FIT_LOWER_LEFT": [[-6, 110], [38, 149.5]],  # lower left branch
    "PH_UPPER": 8000,  ## pressure altitude for upper branch
    "PH_MID": 4000,  ## pressure altitude for mid branch
    "PH_LOWER": 0,  ## pressure altitude for lower branch

}

config_to_dist_15m = {
    "FIT_UPPER_RIGHT": [[608, 540], [700, 759.5], [760, 960]],  # upper right branch
    "FIT_MID_RIGHT": [[620, 419.5], [704, 560], [772, 700.5]],  # mid right branch
    "FIT_LOWER_RIGHT": [[608, 299.5], [680, 381], [780, 520]],  # lower right branch
    "FIT_UPPER_LEFT": [[-18, 459.2], [44, 720]],  # upper left branch
    "FIT_MID_LEFT": [[-18, 320], [42, 479.5]],  # mid left branch
    "FIT_LOWER_LEFT": [[-10, 240.3], [40, 340.3]],  # lower left branch
    "PH_UPPER": 8000,  ## pressure altitude for upper branch
    "PH_MID": 4000,  ## pressure altitude for mid branch
    "PH_LOWER": 0,  ## pressure altitude for lower branch

}

## CALIBRATION LEFT BRANCH (from graph in operatng manual)
# FIT_UPPER_LEFT = [[-18, 459.2], [44, 720]]  # upper branch (15m Hindernis)
# FIT_MID_LEFT = [[-18, 320], [42, 479.5]]  # mid branch (15m Hindernis)
# FIT_LOWER_LEFT = [[-10, 240.3], [40, 340.3]]  # lower branch (15m Hindernis)


@dataclass
class PerformanceResultSet:
    metric_name: str = field()
    metric_value_bare: float = field()
    metric_value_corrected: float = field()
    pressure_altitude: float = field()
    qnh: float = field()
    oat: float = field()
    rw_heading: int = field()
    wind_speed: int = field()
    wind_direction: int = field()
    headwind_component: float = field()
    is_grass: bool = field()
    correction_factor_wind: float = field()
    correction_factor_surface: float = field()



def solve_startroll_0m(weight, rw_heading, temp, alt, wind_speed, wind_direction, qnh, is_grass = False):
    pressure_altitude = elevation2pressurealtitude(elevation_in_feet=alt, qnh_in_hPa=qnh)
    _, right_branch = get_model_branches(
        performance_metric="startroll_0m",
        pressure_altitude=pressure_altitude,
        temperature=temp,
    )
    dist = right_branch.model()(weight)
    headwind = determine_headwind(rw_heading, wind_speed, wind_direction)
    wind_corr = 0.9**(headwind / 4)
    sfc_corr = 1.07 if is_grass else 1.0
    return PerformanceResultSet(
        metric_name="Startlauf",
        metric_value_bare=dist,
        metric_value_corrected=dist * wind_corr * sfc_corr,
        pressure_altitude=pressure_altitude,
        correction_factor_surface=sfc_corr,
        correction_factor_wind=wind_corr,
        qnh=qnh,
        oat=temp,
        rw_heading=rw_heading,
        wind_direction=wind_direction,
        wind_speed=wind_speed,
        headwind_component=headwind,
        is_grass=is_grass,
    )

    # config = None
    # if mode == "0m":
    #     config = config_to_dist
    # elif mode == "15m":
    #     config = config_to_dist_15m
    # else:
    #     raise NotImplementedError(f"mode '{mode}' unknown.")
    # param_model = build_param_model(config)
    # pressure_altitude = elevation2pressurealtitude(elevation_in_feet=alt, qnh_in_hPa=qnh)
    # model_left = select_model_left_branch(pressure_altitude, param_model)
    # init_value = model_left.model()(temp)
    # headwind = determine_headwind(rw_heading, wind_speed, wind_direction)
    # wind_corr = 0.9**(headwind / 4)
    # sfc_corr = 1.0
    # if mode == "0m":
    #     sfc_corr = 1.07 if is_grass else 1.0
    # elif mode == "15m":
    #     sfc_corr = 1.15 if is_grass else 1.0
    # print(f"correction factor = {wind_corr * sfc_corr}")
    # return select_model_right_branch(init_value, param_model).model()(weight) * wind_corr * sfc_corr

def solve_startroll_15m(weight, rw_heading, temp, alt, wind_speed, wind_direction, qnh, is_grass = False):
    pressure_altitude = elevation2pressurealtitude(elevation_in_feet=alt, qnh_in_hPa=qnh)
    _, right_branch = get_model_branches(
        performance_metric="startroll_15m",
        pressure_altitude=pressure_altitude,
        temperature=temp,
    )
    dist = right_branch.model()(weight)
    headwind = determine_headwind(rw_heading, wind_speed, wind_direction)
    wind_corr = 0.9**(headwind / 4)
    sfc_corr = 1.15 if is_grass else 1.0
    return PerformanceResultSet(
        metric_name="Startstrecke über 15m Hindernis",
        metric_value_bare=dist,
        metric_value_corrected=dist * wind_corr * sfc_corr,
        pressure_altitude=pressure_altitude,
        correction_factor_surface=sfc_corr,
        correction_factor_wind=wind_corr,
        qnh=qnh,
        oat=temp,
        rw_heading=rw_heading,
        wind_direction=wind_direction,
        wind_speed=wind_speed,
        headwind_component=headwind,
        is_grass=is_grass,
    )

def solve_landingroll_0m(weight, rw_heading, temp, alt, wind_speed, wind_direction, qnh, is_grass = False):
    pressure_altitude = elevation2pressurealtitude(elevation_in_feet=alt, qnh_in_hPa=qnh)
    _, right_branch = get_model_branches(
        performance_metric="landingroll_0m",
        pressure_altitude=pressure_altitude,
        temperature=temp,
    )
    dist = right_branch.model()(weight)
    headwind = determine_headwind(rw_heading, wind_speed, wind_direction)
    wind_corr = 0.9**(headwind / 4)
    sfc_corr = 1.2 if is_grass else 1.0
    return PerformanceResultSet(
        metric_name="Landelauf",
        metric_value_bare=dist,
        metric_value_corrected=dist * wind_corr * sfc_corr,
        pressure_altitude=pressure_altitude,
        correction_factor_surface=sfc_corr,
        correction_factor_wind=wind_corr,
        qnh=qnh,
        oat=temp,
        rw_heading=rw_heading,
        wind_direction=wind_direction,
        wind_speed=wind_speed,
        headwind_component=headwind,
        is_grass=is_grass,
    )

def solve_landingroll_15m(weight, rw_heading, temp, alt, wind_speed, wind_direction, qnh, is_grass = False):
    pressure_altitude = elevation2pressurealtitude(elevation_in_feet=alt, qnh_in_hPa=qnh)
    _, right_branch = get_model_branches(
        performance_metric="landingroll_15m",
        pressure_altitude=pressure_altitude,
        temperature=temp,
    )
    dist = right_branch.model()(weight)
    headwind = determine_headwind(rw_heading, wind_speed, wind_direction)
    wind_corr = 0.9**(headwind / 4)
    sfc_corr = 1.07 if is_grass else 1.0
    return PerformanceResultSet(
        metric_name="Landestrecke über 15m Hindernis",
        metric_value_bare=dist,
        metric_value_corrected=dist * wind_corr * sfc_corr,
        pressure_altitude=pressure_altitude,
        correction_factor_surface=sfc_corr,
        correction_factor_wind=wind_corr,
        qnh=qnh,
        oat=temp,
        rw_heading=rw_heading,
        wind_direction=wind_direction,
        wind_speed=wind_speed,
        headwind_component=headwind,
        is_grass=is_grass,
    )


def determine_headwind(rw_heading, wind_speed, wind_direction) -> float:
    dphi = (wind_direction - rw_heading) / 180 * math.pi
    return wind_speed * math.cos(dphi)

def detemine_pressure_altitude(qnh, alt):
    return alt


def select_model_right_branch(initial_value, param_model, boundary_condition = None):
    model = FirstOrderRational(*[[600, 230], [700, 334], [780, 432]])  # just a dummy
    model.reset_model({
        k: param_model[k].model()(initial_value)
        for k in ('a', 'b', 'c')
    })
    if boundary_condition is not None:
            y0 = model.model()(boundary_condition[0])
            params = model.parameters()
            model.reset_model({
                'a': params['a'] + (boundary_condition[1] - y0),
                'b': params['b'],
                'c': params['c'],
            })
    return model


def select_model_left_branch(pressure_altitude, param_model):
    model = FirstOrderPolynomial(*[[-14, 209], [48, 321]])  # just a dummy
    model.reset_model({
        k: param_model[k].model()(pressure_altitude)
        for k in ('m', 't')
    })
    return model


def build_param_model(config):

    # fit models
    fit_right_upper = FirstOrderRational(*config["FIT_UPPER_RIGHT"])
    pu_right = fit_right_upper.parameters()
    fit_right_mid = FirstOrderRational(*config["FIT_MID_RIGHT"])
    pm_right = fit_right_mid.parameters()
    fit_right_lower = FirstOrderRational(*config["FIT_LOWER_RIGHT"])
    pl_right = fit_right_lower.parameters()

    fit_left_upper = FirstOrderPolynomial(*config["FIT_UPPER_LEFT"])
    pu_left = fit_left_upper.parameters()
    fit_left_mid = FirstOrderPolynomial(*config["FIT_MID_LEFT"])
    pm_left = fit_left_mid.parameters()
    fit_left_lower = FirstOrderPolynomial(*config["FIT_LOWER_LEFT"])
    pl_left = fit_left_lower.parameters()

    # fit model for parameters
    pfit = {}
    for k, _ in pu_right.items():
        pfit[k] = [
            [fit_right_lower.model()(600), pl_right[k]],
            [fit_right_mid.model()(600), pm_right[k]],
            [fit_right_upper.model()(600), pu_right[k]],
        ]
    for k, _ in pu_left.items():
        pfit[k] = [
            [config["PH_LOWER"], pl_left[k]],
            [config["PH_MID"], pm_left[k]],
            [config["PH_UPPER"], pu_left[k]],
        ]
    
    # get models for parameters
    param_model = {}
    for k, pts in pfit.items():
        if k in ('b', 'c'):
            param_model[k] = SecondOrderRational(*pts)
        else:
            param_model[k] = SecondOrderPolynomial(*pts)
    
    return param_model
