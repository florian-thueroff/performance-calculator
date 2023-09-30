from dataclasses import dataclass, field
from performance.solver import PerformanceResultSet
from weightbalance.solver import WBResultSet

@dataclass
class SummaryResultSet:
    icao_code: str = field()
    time: str = field()
    qnh: float = field()
    pressure_altitude: float = field()
    elevation: float = field()
    oat: float = field()
    rw_heading: int = field()
    wind_speed: int = field()
    wind_direction: int = field()
    headwind_component: float = field()


class HTMLRenderer:

    def __init__(self):
        self.wb_departure = None
        self.wb_destination = None
        self.wb_alternate = None
        self.dep_s0 = None
        self.dep_s15 = None
        self.dest_l0 = None
        self.dest_l15 = None
        self.alt_l0 = None
        self.alt_l15 = None
        self.summary = None
    
    def add_summary(self, dep: SummaryResultSet, dest: SummaryResultSet, alt: SummaryResultSet):
        self.summary = f"""<h1>Planned Flight</h1>
        <table class="border" border="2" cellpadding="10" cellspacing="5">
            <tr>
                <th class="color" width="40%">Key Figure</th>
                <th class="color" width="20%">Departure ({dep.icao_code})</th>
                <th class="color" width="20%">Destination ({dest.icao_code})</th>
                <th class="color" width="20%">Alternate ({alt.icao_code})</th>
            </tr>
            <tr class="main">
                <td>Time of Departure / Arrival</td>
                <td>{dep.time}</td>
                <td>{dest.time}</td>
                <td>{alt.time}</td>
            </tr>
            <tr class="main">
                <td>Outside Air Temperature</td>
                <td>{round(dep.oat)}°C</td>
                <td>{round(dest.oat)}°C</td>
                <td>{round(alt.oat)}°C</td>
            </tr>
            <tr class="main">
                <td>QNH</td>
                <td>{round(dep.qnh)} hPa</td>
                <td>{round(dest.qnh)} hPa</td>
                <td>{round(alt.qnh)} hPa</td>
            </tr>
            <tr class="main">
                <td>Field Elevation</td>
                <td>{round(dep.elevation)} ft</td>
                <td>{round(dest.elevation)} ft</td>
                <td>{round(alt.elevation)} ft</td>
            </tr>
            <tr class="main">
                <td>Pressure Altitude</td>
                <td>{round(dep.pressure_altitude)} ft</td>
                <td>{round(dest.pressure_altitude)} ft</td>
                <td>{round(alt.pressure_altitude)} ft</td>
            </tr>
            <tr class="main">
                <td>Runway Heading</td>
                <td>{round(dep.rw_heading)}°</td>
                <td>{round(dest.rw_heading)}°</td>
                <td>{round(alt.rw_heading)}°</td>
            </tr>
            <tr class="main">
                <td>Wind</td>
                <td>{round(dep.wind_direction)}°@{round(dep.wind_speed)}kt</td>
                <td>{round(dest.wind_direction)}°@{round(dest.wind_speed)}kt</td>
                <td>{round(alt.wind_direction)}°@{round(alt.wind_speed)}kt</td>
            </tr>
            <tr class="main">
                <td>Headwind Component</td>
                <td>{round(dep.headwind_component)} kt</td>
                <td>{round(dest.headwind_component)} kt</td>
                <td>{round(alt.headwind_component)} kt</td>
            </tr>
        </table>"""
    
    def add_perf(self, metric: str, margin: float, res: PerformanceResultSet):
        img=""
        if metric == "Start Roll":
            img = "s0m_dep.png"
        elif metric == "Start Roll Over 50ft Obstacle":
            img = "s15m_dep.png"
        elif metric == "Landing Roll (Destination)":
            img = "l0m_dest.png"
        elif metric == "Landing Roll Over 50ft Obstacle (Destination)":
            img = "l15m_dest.png"
        elif metric == "Landing Roll (Alternate)":
            img = "l0m_alt.png"
        elif metric == "Landing Roll Over 50ft Obstacle (Alternate)":
            img = "l15m_alt.png"
        code = f"""<h1>{metric}</h1>
        <img src="{img}" format="landscape">
        <table class="border" border="2" cellpadding="10" cellspacing="5">
            <tr>
                <th class="color" width="20%">Key Figure</th>
                <th class="color" width="15%">Value</th>
                <th class="color" width="45%">Description</th>
            </tr>
            <tr class="main">
                <td>Clean Value</td>
                <td>{round(res.metric_value_bare)} m</td>
                <td>Landing roll at 0 knots wind and concrete surface</td>
            </tr>
            <tr class="main">
                <td>Wind Correction</td>
                <td>{f'{res.correction_factor_wind:.2f}'}</td>
                <td>Multiplicative factor accounting for wind</td>
            </tr>
            <tr class="main">
                <td>Surface Correction</td>
                <td>{f'{res.correction_factor_surface:.2f}'}</td>
                <td>Multiplicative factor accounting for runway surface</td>
            </tr>
            <tr class="main">
                <td class="bold">Expected Value</td>
                <td class="bold">{round(res.metric_value_corrected)} m</td>
                <td>Landing roll at forecast wind and actual runway surface</td>
            </tr>
            <tr class="main">
                <td>Safety Margin</td>
                <td>{round(margin)}%</td>
                <td>Safety margin to add to expected landing roll</td>
            </tr>
            <tr class="main">
                <td class="emph">Safe Value</td>
                <td class="emph">{round(res.metric_value_corrected * (1 + margin/100.0))} m</td>
                <td>Safe value for landing roll</td>
            </tr>
        </table>"""
        if metric == "Start Roll":
            self.dep_s0 = code
        elif metric == "Start Roll Over 50ft Obstacle":
            self.dep_s15 = code
        elif metric == "Landing Roll (Destination)":
            self.dest_l0 = code
        elif metric == "Landing Roll Over 50ft Obstacle (Destination)":
            self.dest_l15 = code
        elif metric == "Landing Roll (Alternate)":
            self.alt_l0 = code
        elif metric == "Landing Roll Over 50ft Obstacle (Alternate)":
            self.alt_l15 = code
    
    def add_wb(self, airfield: str, wb_res: WBResultSet):
        code = f"""
<h1>Weight and Balance ({airfield})</h1>
        <img src="wb_{airfield}.png" format="portrait">

        <table class="border" border="2" cellpadding="10" cellspacing="5">
            <tr>
                <th class="color" width="50%">Key Figure</th>
                <th class="color" width="25%">Mass</th>
                <th class="color" width="25%">Momentum</th>
            </tr>
            <tr class="main">
                <td>Empty Aircraft</td>
                <td>{f'{wb_res.weight_empty:.1f}'} kg</td>
                <td>{f'{wb_res.momentum_empty:.1f}'} kgm</td>
            </tr>
            <tr class="main">
                <td>Pilot and Passenger</td>
                <td>{f'{wb_res.weight_pp:.1f}'} kg</td>
                <td>{f'{wb_res.momentum_pp:.1f}'} kgm</td>
            </tr>
            <tr class="main">
                <td>Fuel ({f'{wb_res.volume_fuel:.1f}'} l)</td>
                <td>{f'{wb_res.weight_fuel:.1f}'} kg</td>
                <td>{f'{wb_res.momentum_fuel:.1f}'} kgm</td>
            </tr>
            <tr class="main">
                <td>Baggage</td>
                <td>{f'{wb_res.weight_baggage:.1f}'} kg</td>
                <td>{f'{wb_res.momentum_baggage:.1f}'} kgm</td>
            </tr>
            <tr>
                <td colspan="2" align="right"><b>TOTAL MASS</b></td>
                <td colspan="1" align="right" class="border center">{f'{wb_res.weight_total:.1f}'} kg</td>
            </tr>
            <tr>
                <td colspan="2" align="right"><b>TOTAL MOMENTUM</b></td>
                <td colspan="1" align="right" class="border center">{f'{wb_res.momentum_total:.1f}'} kgm</td>
            </tr>
            <tr>
                <td colspan="2" align="right"><b>WITHIN LIMITS</b></td>
                <td colspan="1" align="right" class="border center {'passed' if wb_res.within_limits else 'failed'}">{'YES' if wb_res.within_limits else 'NO'}</td>
            </tr>
        </table>
        """
        if airfield == "Departure":
            self.wb_departure = code
        elif airfield == "Destination":
            self.wb_destination = code
        elif airfield == "Alternate":
            self.wb_alternate = code

    def render(self) -> str:
        code = f"""<!DOCTYPE html>
            <html lang="en">

            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Document</title>
                <style>
                    body {{
                        background: rgb(204, 204, 204);
                    }}

                    page {{
                        background: white;
                        display: block;
                        margin: 0 auto;
                        margin-bottom: 0.5cm;
                        box-shadow: 0 0 0.5cm rgba(0, 0, 0, 0.5);
                        padding: 2cm;
                        box-sizing: border-box;
                    }}

                    page[size="A4"] {{
                        width: 21cm;
                        height: 29.7cm;
                    }}

                    page[size="A4"][layout="landscape"] {{
                        width: 29.7cm;
                        height: 21cm;
                    }}

                    page[size="A3"] {{
                        width: 29.7cm;
                        height: 42cm;
                    }}

                    page[size="A3"][layout="landscape"] {{
                        width: 42cm;
                        height: 29.7cm;
                    }}

                    page[size="A5"] {{
                        width: 14.8cm;
                        height: 21cm;
                    }}

                    page[size="A5"][layout="landscape"] {{
                        width: 21cm;
                        height: 14.8cm;
                    }}

                    img {{
                        display: block;
                        margin-left: auto;
                        margin-right: auto;
                    }}

                    img[format="portrait"] {{
                        height: 12.4cm;
                    }}

                    img[format="landscape"] {{
                        width: 17cm;
                    }}

                    table {{
                        width: 17cm;
                        margin-top: 1.5cm;
                    }}

                    .color {{
                        background-color: lightblue;
                    }}

                    tr.main:nth-child(odd) td {{
                        background-color: rgba(211, 211, 211, 0.429);
                    }}

                    .border {{
                        border: 2px double;
                        border-collapse: collapse;
                    }}

                    .center {{
                        text-align: center;
                        font-weight: 800;
                    }}

                    .passed {{
                        background-color: aquamarine;
                        color: darkgreen;
                    }}

                    .failed {{
                        background-color: tomato;
                        color: darkred;
                    }}

                    .bold {{
                        font-weight: 800;
                    }}

                    .emph {{
                        font-weight: 800;
                        font-size: 1.3em;
                    }}

                    @media print {{

                        body,
                        page {{
                            background: white;
                            margin: 0;
                            box-shadow: 0;
                        }}
                    }}
                </style>
            </head>

            <body>"""
        if self.summary:
            code += f"""<page size="A4">
                    {self.summary}
                </page>"""
        if self.dep_s0:
            code += f"""<page size="A4">
                    {self.dep_s0}
                </page>"""
        if self.dep_s15:
            code += f"""<page size="A4">
                    {self.dep_s15}
                </page>"""
        if self.dest_l0:
            code += f"""<page size="A4">
                    {self.dest_l0}
                </page>"""
        if self.dest_l15:
            code += f"""<page size="A4">
                    {self.dest_l15}
                </page>"""
        if self.alt_l0:
            code += f"""<page size="A4">
                    {self.alt_l0}
                </page>"""
        if self.alt_l15:
            code += f"""<page size="A4">
                    {self.alt_l15}
                </page>"""
        if self.wb_departure:
            code += f"""<page size="A4">
                    {self.wb_departure}
                </page>"""
        if self.wb_destination:
            code += f"""<page size="A4">
                    {self.wb_destination}
                </page>"""
        if self.wb_alternate:
            code += f"""<page size="A4">
                    {self.wb_alternate}
                </page>"""
        code += """
            </body>
            </html>"""
        return code


def print_summary(wb_res: WBResultSet):
    return f"""<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <style>
        body {{
            background: rgb(204, 204, 204);
        }}

        page {{
            background: white;
            display: block;
            margin: 0 auto;
            margin-bottom: 0.5cm;
            box-shadow: 0 0 0.5cm rgba(0, 0, 0, 0.5);
            padding: 2cm;
            box-sizing: border-box;
        }}

        page[size="A4"] {{
            width: 21cm;
            height: 29.7cm;
        }}

        page[size="A4"][layout="landscape"] {{
            width: 29.7cm;
            height: 21cm;
        }}

        page[size="A3"] {{
            width: 29.7cm;
            height: 42cm;
        }}

        page[size="A3"][layout="landscape"] {{
            width: 42cm;
            height: 29.7cm;
        }}

        page[size="A5"] {{
            width: 14.8cm;
            height: 21cm;
        }}

        page[size="A5"][layout="landscape"] {{
            width: 21cm;
            height: 14.8cm;
        }}

        img {{
            display: block;
            margin-left: auto;
            margin-right: auto;
        }}

        img[format="portrait"] {{
            height: 12.4cm;
        }}

        img[format="landscape"] {{
            width: 17cm;
        }}

        table {{
            width: 17cm;
            margin-top: 1.5cm;
        }}

        .color {{
            background-color: lightblue;
        }}

        tr.main:nth-child(odd) td {{
            background-color: rgba(211, 211, 211, 0.429);
        }}

        .border {{
            border: 2px double;
            border-collapse: collapse;
        }}

        .center {{
            text-align: center;
            font-weight: 800;
        }}

        .passed {{
            background-color: aquamarine;
            color: darkgreen;
        }}

        .failed {{
            background-color: tomato;
            color: darkred;
        }}

        @media print {{

            body,
            page {{
                background: white;
                margin: 0;
                box-shadow: 0;
            }}
        }}
    </style>
</head>

<body>
    <page size="A4">
        <h1>Weight and Balance (Departure)</h1>
        <img src="wb.png" format="portrait">

        <table class="border" border="2" cellpadding="10" cellspacing="5">
            <tr>
                <th class="color" width="50%">Key Figure</th>
                <th class="color" width="25%">Mass</th>
                <th class="color" width="25%">Momentum</th>
            </tr>
            <tr class="main">
                <td>Empty Aircraft</td>
                <td>{f'{wb_res.weight_empty:.1f}'} kg</td>
                <td>{f'{wb_res.momentum_empty:.1f}'} kgm</td>
            </tr>
            <tr class="main">
                <td>Pilot and Passenger</td>
                <td>{f'{wb_res.weight_pp:.1f}'} kg</td>
                <td>{f'{wb_res.momentum_pp:.1f}'} kgm</td>
            </tr>
            <tr class="main">
                <td>Fuel ({f'{wb_res.volume_fuel:.1f}'} l)</td>
                <td>{f'{wb_res.weight_fuel:.1f}'} kg</td>
                <td>{f'{wb_res.momentum_fuel:.1f}'} kgm</td>
            </tr>
            <tr class="main">
                <td>Baggage</td>
                <td>{f'{wb_res.weight_baggage:.1f}'} kg</td>
                <td>{f'{wb_res.momentum_baggage:.1f}'} kgm</td>
            </tr>
            <tr>
                <td colspan="2" align="right"><b>TOTAL MASS</b></td>
                <td colspan="1" align="right" class="border center">{f'{wb_res.weight_total:.1f}'} kg</td>
            </tr>
            <tr>
                <td colspan="2" align="right"><b>TOTAL MOMENTUM</b></td>
                <td colspan="1" align="right" class="border center">{f'{wb_res.momentum_total:.1f}'} kgm</td>
            </tr>
            <tr>
                <td colspan="2" align="right"><b>WITHIN LIMITS</b></td>
                <td colspan="1" align="right" class="border center {'passed' if wb_res.within_limits else 'failed'}">{'YES' if wb_res.within_limits else 'NO'}</td>
            </tr>
        </table>

    </page>

    <page size="A4">
        <h1>Das ist noch eine Überschrift</h1>
        <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Ut, doloribus temporibus consequuntur vero non fugiat consequatur aperiam nobis qui! Ducimus odit aliquam quasi dolores corporis! Ratione sapiente voluptas repellat odio.</p>
    </page>
</body>

</html>"""
