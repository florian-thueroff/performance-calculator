import math
import shutil
import tempfile
from pydantic import BaseModel, Field
import pdfkit
from latex.pdf import generate_pdf
from performance.plotter import plot_landingroll, plot_landingroll_over_15m_obstacle, plot_startroll, plot_startroll_over_15m_obstacle
from performance.solver import solve_startroll_0m, solve_startroll_15m, solve_landingroll_0m, solve_landingroll_15m
from performance.models import rb_landingroll_15, rb_landingroll_0

from fastapi import FastAPI
from fastapi import Response
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from weightbalance.plotter import plot_wb

from weightbalance.solver import solve_wb

# router = APIRouter()
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PerformanceParameters(BaseModel):

    weight: int = Field(
        title="Aircraft weight", 
        description="Total weight of the aircraft"
    )

    wind_speed: int = Field(
        title="Wind speed",
        description="Wind speed in knots",
    )

    wind_direction: int = Field(
        title="Wind direction",
        description="Wind direction in degrees",
    )

    alt: int = Field(
        title="Airfield elevation",
        description="Elevation of the airfield in feet MSL",
    )

    temp: int = Field(
        title="Outside air temperature",
        description="Outside air temperature in degress Celsius",
    )

    qnh: float = Field(
        title="QNH",
        description="Airfield QNH",
    )

    rw_heading: int = Field(
        title="Runway heading",
        description="Runway heading in degress (0 ... 359)",
    )

    safety_factor: int = Field(
        default=0,
        title="Safety factor",
        description="Safety factor (interpreted as integer percentage) by which computed start and landing distances are increased. 0 means no safetyl factor applied",
    )


class Airfield(BaseModel):

    name: str = Field(
        title="Airfield name", 
        description="Name of the airfield"
    )

    code: str = Field(
        title="Airfield code", 
        description="ICAO code of the airfield"
    )

    parameters: PerformanceParameters = Field(
        title="Performace parameters", 
        description="Performace parameters for the airfield at the time of take-off or landing"
    )


class RequestData(BaseModel):

    departure: Airfield = Field(
        title="Departure airfield", 
        description="Departure airfield"
    )

    destination: Airfield = Field(
        title="Destination airfield", 
        description="Destination airfield"
    )

    departure_time: str = Field(
        title="Departure time", 
        description="Planned departure time"
    )

    arrival_time: str = Field(
        title="Arrival time", 
        description="Planned arrival time"
    )



@app.post(
    "/performance/",
    tags=["Performance Calculations"],
    summary="Convert LaTeX to PDF",
    description="Converts an array of exercise / solution LaTeX codes to PDF using pdflatex.",
)
async def calc_perf(
    config: RequestData,
    response: Response,
) -> bytes:

    plot_startroll(
        weight=config.departure.parameters.weight, 
        temp=config.departure.parameters.temp, 
        alt=config.departure.parameters.alt,
        qnh=config.departure.parameters.qnh,
    )

    plot_startroll_over_15m_obstacle(
        weight=config.departure.parameters.weight, 
        temp=config.departure.parameters.temp, 
        alt=config.departure.parameters.alt,
        qnh=config.departure.parameters.qnh,
    )

    plot_landingroll_over_15m_obstacle(
        weight=config.destination.parameters.weight, 
        temp=config.destination.parameters.temp, 
        alt=config.destination.parameters.alt,
        qnh=config.destination.parameters.qnh,
    )

    plot_landingroll(
        weight=config.destination.parameters.weight, 
        temp=config.destination.parameters.temp, 
        alt=config.destination.parameters.alt,
        qnh=config.destination.parameters.qnh,
    )

    start_0 = solve_startroll_0m(
        weight=config.departure.parameters.weight, 
        rw_heading=config.departure.parameters.rw_heading, 
        temp=config.departure.parameters.temp, 
        alt=config.departure.parameters.alt, 
        wind_speed=config.departure.parameters.wind_speed, 
        wind_direction=config.departure.parameters.wind_direction,
        qnh=config.departure.parameters.qnh,
    )
    start_15 = solve_startroll_15m(
        weight=config.departure.parameters.weight, 
        rw_heading=config.departure.parameters.rw_heading, 
        temp=config.departure.parameters.temp, 
        alt=config.departure.parameters.alt, 
        wind_speed=config.departure.parameters.wind_speed, 
        wind_direction=config.departure.parameters.wind_direction,
        qnh=config.departure.parameters.qnh,
    )
    landing_0 = solve_landingroll_0m(
        weight=config.destination.parameters.weight, 
        rw_heading=config.destination.parameters.rw_heading, 
        temp=config.destination.parameters.temp, 
        alt=config.destination.parameters.alt, 
        wind_speed=config.destination.parameters.wind_speed, 
        wind_direction=config.destination.parameters.wind_direction,
        qnh=config.destination.parameters.qnh,
    )
    landing_15 = solve_landingroll_15m(
        weight=config.destination.parameters.weight, 
        rw_heading=config.destination.parameters.rw_heading, 
        temp=config.destination.parameters.temp, 
        alt=config.destination.parameters.alt, 
        wind_speed=config.destination.parameters.wind_speed, 
        wind_direction=config.destination.parameters.wind_direction,
        qnh=config.destination.parameters.qnh,
    )

    # computed distances including safety margin (rounded up to the next multiple of 10)
    def roundup(x: float) -> int:
        return math.ceil(x / 10) * 10
    safety_margin_departure: float = 1 + (config.departure.parameters.safety_factor / 100.0)
    safety_margin_destination: float = 1 + (config.destination.parameters.safety_factor / 100.0)
    d_start_roll_0 = roundup(safety_margin_departure * start_0.metric_value_corrected)
    d_start_roll_15 = roundup(safety_margin_departure * start_15.metric_value_corrected)
    d_landing_roll_0 = roundup(safety_margin_destination * landing_0.metric_value_corrected)
    d_landing_roll_15 = roundup(safety_margin_destination * landing_15.metric_value_corrected)
    latex_code = f"""
\\documentclass[12pt, a4paper]{{article}}
\\usepackage{{graphicx}}
\\usepackage[most]{{tcolorbox}}
\\usepackage[most]{{booktabs}}
\\begin{{document}}
                       
\\section{{Routenplanung}}
\\begin{{tabular}}{{p{{0.3\\textwidth}}p{{0.6\\textwidth}}}}\\toprule
\\multicolumn{{2}}{{l}}{{Startflugplatz: {config.departure.name} ({config.departure.code})}} \\\\ \\midrule
Geplante Startzeit & {config.departure_time} \\\\
QNH & {config.departure.parameters.qnh}hPa \\\\
Platzhöhe & {config.departure.parameters.alt}ft \\\\
Druckhöhe & {round(start_0.pressure_altitude)}ft \\\\
Pistenrichtung & {str(config.departure.parameters.rw_heading).zfill(3)} \\\\
Wind & {config.departure.parameters.wind_direction}@{config.departure.parameters.wind_speed}kt \\\\
Gegenwindkomponente & {round(start_0.headwind_component)}kt \\\\ \\midrule 
\\multicolumn{{2}}{{l}}{{Zielflugplatz: {config.destination.name} ({config.destination.code})}} \\\\ \\midrule
Geplante Landezeit & {config.arrival_time} \\\\
QNH & {config.destination.parameters.qnh}hPa \\\\
Platzhöhe & {config.destination.parameters.alt}ft \\\\
Druckhöhe & {round(landing_0.pressure_altitude)}ft \\\\
Pistenrichtung & {str(config.destination.parameters.rw_heading).zfill(3)} \\\\
Wind & {config.destination.parameters.wind_direction}@{config.destination.parameters.wind_speed}kt \\\\
Gegenwindkomponente & {round(landing_0.headwind_component)}kt \\\\ \\bottomrule
\\end{{tabular}}

\\newpage

\\section{{Startlauf}}
\\includegraphics[width=\\textwidth]{{/code/img/startroll_0m.png}}\\\\[1cm]
\\begin{{tabular}}{{p{{0.6\\textwidth}}p{{0.3\\textwidth}}}}\\toprule
Basiswert & \\textbf{{{f"{start_0.metric_value_bare:.2f}"}m}} \\\\ \\midrule
Korrekturfaktor (Gegenwind) & {f"{start_0.correction_factor_wind:.2f}"} \\\\
Korrekturfaktor (Oberfläche) & {f"{start_0.correction_factor_surface:.2f}"} \\\\  \\midrule \\midrule
Korrigierter Wert & \\textbf{{{f"{start_0.metric_value_corrected:.2f}"}m}} \\\\
Sicherheitsmarge & {f"{config.departure.parameters.safety_factor}"}\\% \\\\  \\midrule \\midrule
\\textcolor{{blue}}{{\\textbf{{Startlauf}} (gerundet)}} & \\textcolor{{blue}}{{\\textbf{{{d_start_roll_0}m}}}} \\\\ \\bottomrule
\\end{{tabular}}

\\newpage

\\section{{Startstrecke über 15m Hindernis}}
\\includegraphics[width=\\textwidth]{{/code/img/startroll_15m.png}}\\\\[1cm]
\\begin{{tabular}}{{p{{0.6\\textwidth}}p{{0.3\\textwidth}}}}\\toprule
Basiswert & \\textbf{{{f"{start_15.metric_value_bare:.2f}"}m}} \\\\ \\midrule
Korrekturfaktor (Gegenwind) & {f"{start_15.correction_factor_wind:.2f}"} \\\\
Korrekturfaktor (Oberfläche) & {f"{start_15.correction_factor_surface:.2f}"} \\\\  \\midrule \\midrule
Korrigierter Wert & \\textbf{{{f"{start_15.metric_value_corrected:.2f}"}m}} \\\\
Sicherheitsmarge & {f"{config.departure.parameters.safety_factor}"}\\% \\\\  \\midrule \\midrule
\\textcolor{{blue}}{{\\textbf{{Startstrecke}} (gerundet)}} & \\textcolor{{blue}}{{\\textbf{{{d_start_roll_15}m}}}} \\\\ \\bottomrule
\\end{{tabular}}

\\newpage

\\section{{Landelauf}}
\\includegraphics[width=\\textwidth]{{/code/img/landingroll_0m.png}}\\\\[1cm]
\\begin{{tabular}}{{p{{0.6\\textwidth}}p{{0.3\\textwidth}}}}\\toprule
Basiswert & \\textbf{{{f"{landing_0.metric_value_bare:.2f}"}m}} \\\\ \\midrule
Korrekturfaktor (Gegenwind) & {f"{landing_0.correction_factor_wind:.2f}"} \\\\
Korrekturfaktor (Oberfläche) & {f"{landing_0.correction_factor_surface:.2f}"} \\\\  \\midrule \\midrule
Korrigierter Wert & \\textbf{{{f"{landing_0.metric_value_corrected:.2f}"}m}} \\\\
Sicherheitsmarge & {f"{config.destination.parameters.safety_factor}"}\\% \\\\  \\midrule \\midrule
\\textcolor{{blue}}{{\\textbf{{Landelauf}} (gerundet)}} & \\textcolor{{blue}}{{\\textbf{{{d_landing_roll_0}m}}}} \\\\ \\bottomrule
\\end{{tabular}}

\\newpage

\\section{{Landestrecke über 15m Hindernis}}
\\includegraphics[width=\\textwidth]{{/code/img/landingroll_15m.png}}\\\\[1cm]
\\begin{{tabular}}{{p{{0.6\\textwidth}}p{{0.3\\textwidth}}}}\\toprule
Basiswert & \\textbf{{{f"{landing_15.metric_value_bare:.2f}"}m}} \\\\ \\midrule
Korrekturfaktor (Gegenwind) & {f"{landing_15.correction_factor_wind:.2f}"} \\\\
Korrekturfaktor (Oberfläche) & {f"{landing_15.correction_factor_surface:.2f}"} \\\\  \\midrule \\midrule
Korrigierter Wert & \\textbf{{{f"{landing_15.metric_value_corrected:.2f}"}m}} \\\\
Sicherheitsmarge & {f"{config.destination.parameters.safety_factor}"}\\% \\\\  \\midrule \\midrule
\\textcolor{{blue}}{{\\textbf{{Landestrecke}} (gerundet)}} & \\textcolor{{blue}}{{\\textbf{{{d_landing_roll_15}m}}}} \\\\ \\bottomrule
\\end{{tabular}}

                       
\\end{{document}}
    """

    pdf = "/code/output/performance.pdf"
    with tempfile.TemporaryDirectory() as tmpdir:    
        tmp = generate_pdf(source=latex_code, dir=tmpdir)
        shutil.copy(tmp, "/code/output/performance.pdf")


    headers = {
        "Content-Disposition": "inline; filename=performance.pdf"
    }  

    # Return the FileResponse object
    return FileResponse(pdf, media_type="application/pdf", headers=headers)


def test():
    # pdfkit.from_file('assets/html/test.html', 'out.pdf')
    # perm, moment, weight = solve_wb(
    #     baggage_weight_kg=10,
    #     pilot_weight_kg=80,
    #     passenger_weight_kg=75,
    #     fuel_litres=80,
    #     empty_moment_kgm=167.88,
    #     empty_weight_kg=556.5
    # )
    plot_wb(
        baggage_weight_kg=10,
        pilot_weight_kg=80,
        passenger_weight_kg=0,
        fuel_litres=80,
        empty_moment_kgm=167.88,
        empty_weight_kg=556.5
    )
    # print(f"permissibe: {perm}\nmoment: {moment}kgm\nweight:{weight}kg")


if __name__ == '__main__':
    test()
