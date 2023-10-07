from dataclasses import dataclass, field

from model.first_order_polynomial import FirstOrderPolynomial
from weightbalance.constants import A, B, C, D, E, slope_baggage, slope_fuel, slope_pilot_passenger


@dataclass
class WBResultSet:
    weight_pp: float = field()
    weight_baggage: float = field()
    weight_fuel: float = field()
    momentum_pp: float = field()
    momentum_baggage: float = field()
    momentum_fuel: float = field()
    weight_total: float = field()
    momentum_total: float = field()
    within_limits: bool = field()
    momentum_empty: float = field()
    weight_empty: bool = field()
    volume_fuel: float = field()


def wb_permissible(total_weight_kg: float, total_moment_kgm: float) -> bool:
    if total_moment_kgm <= A[0]:
        return False
    if total_moment_kgm <= B[0]:
        g = FirstOrderPolynomial(*[A, B]).model()
        return total_weight_kg < g(total_moment_kgm)
    if total_moment_kgm <= E[0]:
        g = FirstOrderPolynomial(*[B, C]).model()
        return total_weight_kg < g(total_moment_kgm)
    if total_moment_kgm <= C[0]:
        g = FirstOrderPolynomial(*[B, C]).model()
        h = FirstOrderPolynomial(*[E, D]).model()
        return total_weight_kg < g(total_moment_kgm) and total_weight_kg > h(total_moment_kgm)
    if total_moment_kgm < D[0]:
        g = FirstOrderPolynomial(*[E, D]).model()
        return total_weight_kg > g(total_moment_kgm) and total_weight_kg < 780.0
    return False


def solve_wb(
        empty_moment_kgm: float, 
        empty_weight_kg: float, 
        pilot_weight_kg: float, 
        passenger_weight_kg: float, 
        baggage_weight_kg: float, 
        fuel_litres: float
) -> WBResultSet:
    total_weight_kg: float = empty_weight_kg + (fuel_litres * 0.72) + baggage_weight_kg + pilot_weight_kg + passenger_weight_kg
    trafo_pilot_passenger = FirstOrderPolynomial(*[[0,0], [1,1]])
    trafo_fuel = FirstOrderPolynomial(*[[0,0], [1,1]])
    trafo_baggage = FirstOrderPolynomial(*[[0,0], [1,1]])
    trafo_pilot_passenger.reset_model({'m': slope_pilot_passenger, 't': empty_moment_kgm})
    trafo_fuel.reset_model({'m': slope_fuel, 't': trafo_pilot_passenger.model()(pilot_weight_kg + passenger_weight_kg)})
    trafo_baggage.reset_model({'m': slope_baggage, 't': trafo_fuel.model()(fuel_litres)})
    total_moment_kgm = trafo_baggage.model()(baggage_weight_kg)

    return WBResultSet(
        within_limits=wb_permissible(total_weight_kg=total_weight_kg, total_moment_kgm=total_moment_kgm),
        momentum_baggage=trafo_baggage.model()(baggage_weight_kg) - trafo_fuel.model()(fuel_litres),
        momentum_fuel=trafo_fuel.model()(fuel_litres) - trafo_pilot_passenger.model()(pilot_weight_kg + passenger_weight_kg),
        momentum_pp=trafo_pilot_passenger.model()(pilot_weight_kg + passenger_weight_kg) - empty_moment_kgm,
        momentum_total=total_moment_kgm,
        weight_baggage=baggage_weight_kg,
        weight_fuel=fuel_litres*0.72,
        weight_pp=pilot_weight_kg+passenger_weight_kg,
        weight_total=total_weight_kg,
        weight_empty=empty_weight_kg,
        momentum_empty=empty_moment_kgm,
        volume_fuel=fuel_litres,
    )
