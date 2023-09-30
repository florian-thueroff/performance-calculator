import math
import os
from performance.models import get_model_branches

from utils.converter import elevation2pressurealtitude
from utils.plotter import Plotter, PlotterSetup


def plot_startroll(weight, temp, alt, qnh, folder = "", file = ""):

    pressure_altitude = elevation2pressurealtitude(elevation_in_feet=alt, qnh_in_hPa=qnh)
    
    left_branch, right_branch = get_model_branches(
        performance_metric="startroll_0m",
        pressure_altitude=pressure_altitude,
        temperature=temp,
    )

    m = left_branch.parameters()['m']
    model_left = left_branch.model()
    model_right = right_branch.model()



    plot_config = PlotterSetup(
        bg_file="bg_startroll_0m.png",
        bg_alpha=0.5,
        x_dim=[0, 800],
        y_dim=[100,500],
        x_ticks=(
            [0,100,200,300,400,500,600,700,800], 
            ['-20°C', '0°C', '20°C', '40°C', '620kg', '660kg', '700kg', '740kg', '780kg']
        ),
        enforce_original_aspect_ratio=True
    )
    plotter = Plotter(config=plot_config)

    # left hand side plot
    plotter.plot(
        model=model_left,
        x0=-20,
        x1=temp,
        x_transform=lambda x: 5*(x+20),
        color='r',
    )
    plotter.add_arrow(
        x=temp,
        y=model_left(temp),
        dx=50-temp,
        dy=0,
        color='red',
        x_transform=lambda x: 5*(x+20),
    )

    # right hand side plot
    plotter.plot(
        model=model_right,
        x0=600,
        x1=weight,
        x_transform=lambda x: 5*(x-460)/2,
        color='r',
    )
    plotter.add_arrow(
        x=weight,
        y=model_right(weight),
        dx=780-weight,
        dy=0,
        color='red',
        x_transform=lambda x: 5*(x-460)/2,
    )

    # Decorations
    plotter.add_line(  # separator line (temp / mass)
        x0=50,
        y0=100,
        x1=50,
        y1=500,
        color='black',
        x_transform=lambda x: 5*(x+20),
    )
    plotter.add_text_label(  # pressure altitude
        x=(temp-20)/2,
        y=model_left((temp-20)/2),
        text=f"{round(pressure_altitude)} ft",
        rotation=math.atan(m/5) / 2.0 / math.pi * 360,
        color='red',
        x_transform=lambda x: 5*(x+20),
        verticalalignment='bottom',
    )
    plotter.add_line(  # temperature (line)
        x0=temp,
        y0=100,
        x1=temp,
        y1=500,
        color='blue',
        x_transform=lambda x: 5*(x+20),
    )
    plotter.add_text_label(  # temperature (label)
        x=temp,
        y=505,
        text=f"{temp}°C",
        color='blue',
        x_transform=lambda x: 5*(x+20),
        verticalalignment='bottom',
    )
    plotter.add_line(  # weight (line)
        x0=weight,
        y0=100,
        x1=weight,
        y1=500,
        color='blue',
        x_transform=lambda x: 5*(x-460)/2,
    )
    plotter.add_text_label(  # weight (label)
        x=weight,
        y=505,
        text=f"{weight}kg",
        color='blue',
        x_transform=lambda x: 5*(x-460)/2,
        verticalalignment='bottom',
    )
    plotter.add_text_label(  # result
        x=810,
        y=model_right(weight),
        text=f"{round(model_right(weight))}m",
        color='red',
        horizontalalignment='left',
    )

    # plotter.save(os.path.join("/code","img", "startroll_0m.png"))
    plotter.save(os.path.join(folder, f"{file}.png"))


def plot_startroll_over_15m_obstacle(weight, temp, alt, qnh, folder="", file=""):
    
    pressure_altitude = elevation2pressurealtitude(elevation_in_feet=alt, qnh_in_hPa=qnh)
    
    left_branch, right_branch = get_model_branches(
        performance_metric="startroll_15m",
        pressure_altitude=pressure_altitude,
        temperature=temp,
    )

    m = left_branch.parameters()['m']
    model_left = left_branch.model()
    model_right = right_branch.model()

    plot_config = PlotterSetup(
        bg_file="bg_startroll_15m.png",
        bg_alpha=0.5,
        x_dim=[0, 800],
        y_dim=[200,1000],
        x_ticks=(
            [0,100,200,300,400,500,600,700,800], 
            ['-20°C', '0°C', '20°C', '40°C', '620kg', '660kg', '700kg', '740kg', '780kg']
        ),
        enforce_original_aspect_ratio=True
    )
    plotter = Plotter(config=plot_config)

    # left hand side plot
    plotter.plot(
        model=model_left,
        x0=-20,
        x1=temp,
        x_transform=lambda x: 5*(x+20),
        color='r',
    )
    plotter.add_arrow(
        x=temp,
        y=model_left(temp),
        dx=50-temp,
        dy=0,
        color='red',
        x_transform=lambda x: 5*(x+20),
    )

    # right hand side plot
    plotter.plot(
        model=model_right,
        x0=600,
        x1=weight,
        x_transform=lambda x: 5*(x-460)/2,
        color='r',
    )
    plotter.add_arrow(
        x=weight,
        y=model_right(weight),
        dx=780-weight,
        dy=0,
        color='red',
        x_transform=lambda x: 5*(x-460)/2,
    )

    # Decorations
    plotter.add_line(  # separator line (temp / mass)
        x0=50,
        y0=200,
        x1=50,
        y1=1000,
        color='black',
        x_transform=lambda x: 5*(x+20),
    )
    plotter.add_text_label(  # pressure altitude
        x=(temp-20)/2,
        y=model_left((temp-20)/2),
        text=f"{round(pressure_altitude)} ft",
        rotation=math.atan(m/5) / 2.0 / math.pi * 360,
        color='red',
        x_transform=lambda x: 5*(x+20),
        verticalalignment='bottom',
    )
    plotter.add_line(  # temperature (line)
        x0=temp,
        y0=200,
        x1=temp,
        y1=1000,
        color='blue',
        x_transform=lambda x: 5*(x+20),
    )
    plotter.add_text_label(  # temperature (label)
        x=temp,
        y=1010,
        text=f"{temp}°C",
        color='blue',
        x_transform=lambda x: 5*(x+20),
        verticalalignment='bottom',
    )
    plotter.add_line(  # weight (line)
        x0=weight,
        y0=200,
        x1=weight,
        y1=1000,
        color='blue',
        x_transform=lambda x: 5*(x-460)/2,
    )
    plotter.add_text_label(  # weight (label)
        x=weight,
        y=1010,
        text=f"{weight}kg",
        color='blue',
        x_transform=lambda x: 5*(x-460)/2,
        verticalalignment='bottom',
    )
    plotter.add_text_label(  # result
        x=810,
        y=model_right(weight),
        text=f"{round(model_right(weight))}m",
        color='red',
        horizontalalignment='left',
    )

    # plotter.save(os.path.join("/code","img", "startroll_15m.png"))
    plotter.save(os.path.join(folder, f"{file}.png"))


def plot_landingroll_over_15m_obstacle(weight, temp, alt, qnh, folder="", file=""):
    
    pressure_altitude = elevation2pressurealtitude(elevation_in_feet=alt, qnh_in_hPa=qnh)
    
    left_branch, right_branch = get_model_branches(
        performance_metric="landingroll_15m",
        pressure_altitude=pressure_altitude,
        temperature=temp,
    )

    m = left_branch.parameters()['m']
    model_left = left_branch.model()
    model_right = right_branch.model()

    plot_config = PlotterSetup(
        bg_file="bg_landingroll_15m.png",
        bg_alpha=0.5,
        x_dim=[0, 800],
        y_dim=[325,525],
        x_ticks=(
            [0,100,200,300,400,500,600,700,800], 
            ['-20°C', '0°C', '20°C', '40°C', '620kg', '660kg', '700kg', '740kg', '780kg']
        ),
        enforce_original_aspect_ratio=True
    )
    plotter = Plotter(config=plot_config)

    # left hand side plot
    plotter.plot(
        model=model_left,
        x0=-20,
        x1=temp,
        x_transform=lambda x: 5*(x+20),
        color='r',
    )
    plotter.add_arrow(
        x=temp,
        y=model_left(temp),
        dx=50-temp,
        dy=0,
        color='red',
        x_transform=lambda x: 5*(x+20),
    )

    # right hand side plot
    plotter.plot(
        model=model_right,
        x0=600,
        x1=weight,
        x_transform=lambda x: 5*(x-460)/2,
        color='r',
    )
    plotter.add_arrow(
        x=weight,
        y=model_right(weight),
        dx=780-weight,
        dy=0,
        color='red',
        x_transform=lambda x: 5*(x-460)/2,
    )

    # Decorations
    plotter.add_line(  # separator line (temp / mass)
        x0=50,
        y0=325,
        x1=50,
        y1=525,
        color='black',
        x_transform=lambda x: 5*(x+20),
    )
    plotter.add_text_label(  # pressure altitude
        x=(temp-20)/2,
        y=model_left((temp-20)/2),
        text=f"{round(pressure_altitude)} ft",
        rotation=math.atan(m/5) / 2.0 / math.pi * 360,
        color='red',
        x_transform=lambda x: 5*(x+20),
        verticalalignment='bottom',
    )
    plotter.add_line(  # temperature (line)
        x0=temp,
        y0=325,
        x1=temp,
        y1=525,
        color='blue',
        x_transform=lambda x: 5*(x+20),
    )
    plotter.add_text_label(  # temperature (label)
        x=temp,
        y=530,
        text=f"{temp}°C",
        color='blue',
        x_transform=lambda x: 5*(x+20),
        verticalalignment='bottom',
    )
    plotter.add_line(  # weight (line)
        x0=weight,
        y0=325,
        x1=weight,
        y1=525,
        color='blue',
        x_transform=lambda x: 5*(x-460)/2,
    )
    plotter.add_text_label(  # weight (label)
        x=weight,
        y=530,
        text=f"{weight}kg",
        color='blue',
        x_transform=lambda x: 5*(x-460)/2,
        verticalalignment='bottom',
    )
    plotter.add_text_label(  # result
        x=810,
        y=model_right(weight),
        text=f"{round(model_right(weight))}m",
        color='red',
        horizontalalignment='left',
    )

    # plotter.save(os.path.join("/code","img", "landingroll_15m.png"))
    plotter.save(os.path.join(folder, f"{file}.png"))


def plot_landingroll(weight, temp, alt, qnh, folder="", file=""):
    
    pressure_altitude = elevation2pressurealtitude(elevation_in_feet=alt, qnh_in_hPa=qnh)
    xmin, xmax, ymin, ymax = (0, 800, 140, 300)
    dx = (xmax - xmin) / 8
    
    left_branch, right_branch = get_model_branches(
        performance_metric="landingroll_0m",
        pressure_altitude=pressure_altitude,
        temperature=temp,
    )

    m = left_branch.parameters()['m']
    model_left = left_branch.model()
    model_right = right_branch.model()

    plot_config = PlotterSetup(
        bg_file="bg_landingroll_0m.png",
        bg_alpha=0.5,
        x_dim=[xmin, xmax],
        y_dim=[ymin, ymax],
        x_ticks=(
            [dx * i for i in range(9)], 
            ['-20°C', '0°C', '20°C', '40°C', '620kg', '660kg', '700kg', '740kg', '780kg']
        ),
        enforce_original_aspect_ratio=True
    )
    plotter = Plotter(config=plot_config)

    # left hand side plot
    plotter.plot(
        model=model_left,
        x0=-20,
        x1=temp,
        x_transform=lambda x: 5*(x+20),
        color='r',
    )
    plotter.add_arrow(
        x=temp,
        y=model_left(temp),
        dx=50-temp,
        dy=0,
        color='red',
        x_transform=lambda x: 5*(x+20),
    )

    # right hand side plot
    plotter.plot(
        model=model_right,
        x0=600,
        x1=weight,
        x_transform=lambda x: 5*(x-460)/2,
        color='r',
    )
    plotter.add_arrow(
        x=weight,
        y=model_right(weight),
        dx=780-weight,
        dy=0,
        color='red',
        x_transform=lambda x: 5*(x-460)/2,
    )

    # Decorations
    plotter.add_line(  # separator line (temp / mass)
        x0=50,
        y0=ymin,
        x1=50,
        y1=ymax,
        color='black',
        x_transform=lambda x: 5*(x+20),
    )
    plotter.add_text_label(  # pressure altitude
        x=(temp-20)/2,
        y=model_left((temp-20)/2),
        text=f"{round(pressure_altitude)} ft",
        rotation=math.atan(m/5) / 2.0 / math.pi * 360,
        color='red',
        x_transform=lambda x: 5*(x+20),
        verticalalignment='bottom',
    )
    plotter.add_line(  # temperature (line)
        x0=temp,
        y0=ymin,
        x1=temp,
        y1=ymax,
        color='blue',
        x_transform=lambda x: 5*(x+20),
    )
    plotter.add_text_label(  # temperature (label)
        x=temp,
        y=1.01*ymax,
        text=f"{temp}°C",
        color='blue',
        x_transform=lambda x: 5*(x+20),
        verticalalignment='bottom',
    )
    plotter.add_line(  # weight (line)
        x0=weight,
        y0=ymin,
        x1=weight,
        y1=ymax,
        color='blue',
        x_transform=lambda x: 5*(x-460)/2,
    )
    plotter.add_text_label(  # weight (label)
        x=weight,
        y=1.01*ymax,
        text=f"{weight}kg",
        color='blue',
        x_transform=lambda x: 5*(x-460)/2,
        verticalalignment='bottom',
    )
    plotter.add_text_label(  # result
        x=810,
        y=model_right(weight),
        text=f"{round(model_right(weight))}m",
        color='red',
        horizontalalignment='left',
    )

    # plotter.save(os.path.join("/code","img", "landingroll_0m.png"))
    plotter.save(os.path.join(folder, f"{file}.png"))