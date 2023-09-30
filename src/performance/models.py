from typing import Tuple
from model import Model
from model.first_order_polynomial import FirstOrderPolynomial
from model.first_order_rational import FirstOrderRational
from model.parametric_curve import ParametricCurve
from model.second_order_polynomial import SecondOrderPolynomial
from model.second_order_rational import SecondOrderRational

lb_startroll_0 = ParametricCurve(
    model=FirstOrderPolynomial,
    param_model_dict={
        "m": SecondOrderPolynomial,
        "t": SecondOrderPolynomial,
    },
    branch_points_list=[
        [[-14, 209], [48, 321]],  # upper left branch
        [[-14, 149.5], [40, 210]],  # mid left branch
        [[-6, 110], [38, 149.5]],  # lower left branch
    ],
    branch_params=[8000, 4000, 0],
)
    
rb_startroll_0 = ParametricCurve(
    model=FirstOrderRational,
    param_model_dict={
        "a": SecondOrderPolynomial,
        "b": SecondOrderRational,
        "c": SecondOrderRational,
    },
    branch_points_list=[
        [[600, 230], [700, 334], [780, 432]],  # upper right branch
        [[600, 170], [720, 260], [776, 310]],  # mid right branch
        [[604, 130], [684, 170], [780, 230]],  # lower right branch
    ],
    branch_params=600.0,
)

lb_startroll_15 = ParametricCurve(
    model=FirstOrderPolynomial,
    param_model_dict={
        "m": SecondOrderPolynomial,
        "t": SecondOrderPolynomial,
    },
    branch_points_list=[
        [[-18, 459.2], [44, 720]],  # upper left branch
        [[-18, 320], [42, 479.5]],  # mid left branch
        [[-10, 240.3], [40, 340.3]],  # lower left branch
    ],
    branch_params=[8000, 4000, 0],
)

rb_startroll_15 = ParametricCurve(
    model=FirstOrderRational,
    param_model_dict={
        "a": SecondOrderPolynomial,
        "b": SecondOrderRational,
        "c": SecondOrderRational,
    },
    branch_points_list=[
        [[608, 540], [700, 759.5], [760, 960]],  # upper right branch
        [[620, 419.5], [704, 560], [772, 700.5]],  # mid right branch
        [[608, 299.5], [680, 381], [780, 520]]  # lower right branch
    ],
    branch_params=600.0,
)

lb_landingroll_0 = ParametricCurve(
    model=FirstOrderPolynomial,
    param_model_dict={
        "m": SecondOrderPolynomial,
        "t": SecondOrderPolynomial,
    },
    branch_points_list=[
        [[-20, 191.5], [44, 255]],  # upper left branch
        [[-8, 172], [46, 220]],  # mid left branch
        [[-16, 147.5], [44, 184]],  # lower left branch
    ],
    branch_params=[8000, 4000, 0],
)

rb_landingroll_0 = ParametricCurve(
    model=FirstOrderPolynomial,
    param_model_dict={
        "m": SecondOrderPolynomial,
        "t": SecondOrderPolynomial,
    },
    branch_points_list=[
        [[600, 224], [768, 288]],  # upper right branch
        [[608, 187.5], [740, 228]],  # mid right branch
        [[604, 164], [776, 212]]  # lower right branch
    ],
    branch_params=600.0,
)

lb_landingroll_15 = ParametricCurve(
    model=FirstOrderPolynomial,
    param_model_dict={
        "m": SecondOrderPolynomial,
        "t": SecondOrderPolynomial,
    },
    branch_points_list=[
        [[-18, 415], [24, 485]],  # upper left branch
        [[-14, 375], [48, 459.5]],  # mid left branch
        [[-16, 330], [48, 411.5]],  # lower left branch
    ],
    branch_params=[8000, 4000, 0],
)

rb_landingroll_15 = ParametricCurve(
    model=FirstOrderPolynomial,
    param_model_dict={
        "m": SecondOrderPolynomial,
        "t": SecondOrderPolynomial,
    },
    branch_points_list=[
        [[604, 445], [736, 520.5]],  # upper right branch
        [[612, 410], [760, 485]],  # mid right branch
        [[600, 370], [752, 440]]  # lower right branch
    ],
    branch_params=600.0,
)


def _select_models_from_branches(
    left_branch: ParametricCurve, 
    right_branch: ParametricCurve, 
    pressure_altitude: float,
    temperature: int,
) -> Tuple[Model, Model]:
    left_model = left_branch.get_interpolation(pressure_altitude)
    init_value = left_model.model()(temperature)
    right_model = right_branch.get_interpolation(init_value, boundary_condition=[600, init_value])
    return (left_model, right_model)


def get_model_branches(
    performance_metric: str, 
    pressure_altitude: float, 
    temperature: int, 
) -> Tuple[Model, Model]:
    if performance_metric == "startroll_0m":
        return _select_models_from_branches(
            left_branch=lb_startroll_0,
            right_branch=rb_startroll_0,
            pressure_altitude=pressure_altitude,
            temperature=temperature,
        )
    elif performance_metric == "startroll_15m":
        return _select_models_from_branches(
            left_branch=lb_startroll_15,
            right_branch=rb_startroll_15,
            pressure_altitude=pressure_altitude,
            temperature=temperature,
        )
    elif performance_metric == "landingroll_0m":
        return _select_models_from_branches(
            left_branch=lb_landingroll_0,
            right_branch=rb_landingroll_0,
            pressure_altitude=pressure_altitude,
            temperature=temperature,
        )
    elif performance_metric == "landingroll_15m":
        return _select_models_from_branches(
            left_branch=lb_landingroll_15,
            right_branch=rb_landingroll_15,
            pressure_altitude=pressure_altitude,
            temperature=temperature,
        )
    raise NotImplementedError(f"Unknown performance metric '{performance_metric}'.")

