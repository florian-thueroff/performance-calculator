from model.first_order_polynomial import FirstOrderPolynomial

from weightbalance.constants import A, B, C, D, E, slope_baggage, slope_fuel, slope_pilot_passenger
from matplotlib import pyplot as plt
from matplotlib.patches import ConnectionPatch

from weightbalance.solver import wb_permissible

def set_size(w,h, ax=None):
    """ w, h: width, height in inches """
    if not ax: ax=plt.gca()
    l = ax.figure.subplotpars.left
    r = ax.figure.subplotpars.right
    t = ax.figure.subplotpars.top
    b = ax.figure.subplotpars.bottom
    figw = float(w)/(r-l)
    figh = float(h)/(t-b)
    print(f"Setting (w, h) = ({figw}, {figh})")
    ax.figure.set_size_inches(figw, figh)


def plot_wb(
    empty_moment_kgm: float, 
    empty_weight_kg: float, 
    pilot_weight_kg: float, 
    passenger_weight_kg: float, 
    baggage_weight_kg: float, 
    fuel_litres: float,
    folder: str = "",
    filename: str = "wb",
):
    
    aircraft_weight = empty_weight_kg + pilot_weight_kg+ passenger_weight_kg + baggage_weight_kg + fuel_litres * 0.72
    
    x_extension = 1100
    y_extension = 300
    xtrans = lambda x: x / 550 * x_extension
    ytrans2 = lambda x: x / 200 * y_extension

    img2 = plt.imread("assets/bg_wb_pilotpassenger.png")
    img1 = plt.imread("assets/bg_wb_fuel.png")
    img3 = plt.imread("assets/bg_wb_baggage.png")
    img4 = plt.imread("assets/bg_wb_summary.png")

    
    scale2 = len(img2)/(len(img1)+len(img2)+len(img3)+len(img4))
    
    # scale1 = len(img2)/len(img1)
    scale1 = len(img1)/(len(img1)+len(img2)+len(img3)+len(img4))
    ymax1 = y_extension/scale2*scale1
    ytrans1 = lambda x: x / 125 * ymax1

    # scale3 = len(img2)/len(img3)
    scale3 = len(img3)/(len(img1)+len(img2)+len(img3)+len(img4))
    ymax3 = y_extension/scale2*scale3
    ytrans3 = lambda x: x / 40 * ymax3

    scale4 = len(img4)/(len(img1)+len(img2)+len(img3)+len(img4))
    ymax4 = y_extension/scale2*scale4
    y14 = 400
    y24 = 750 + 9.5/6.0 * 50
    ytrans4 = lambda x: (x - 400) / (y24 - y14) * ymax4

    fig, (ax4, ax3, ax1, ax2) = plt.subplots(4, sharex=True, height_ratios=[scale4, scale3, scale1, scale2])
    # fig, (ax3, ax2) = plt.subplots(2, sharex=True, height_ratios=[1, scale3])

    ax2.imshow(
        img2, 
        extent=[0, x_extension, 0, y_extension], 
        alpha=0.5,
    )
    
    model1 = FirstOrderPolynomial(*[[0,0], [1,1]])
    model1.reset_model({'m': 1 / slope_pilot_passenger, 't': -empty_moment_kgm / slope_pilot_passenger})
    inv_model1 = FirstOrderPolynomial(*[[0,0], [1,1]])
    inv_model1.reset_model({'m': slope_pilot_passenger, 't': empty_moment_kgm})

    dx1 = (inv_model1.model()(pilot_weight_kg + passenger_weight_kg) - empty_moment_kgm) / 500.0
    x1 = [empty_moment_kgm + n * dx1 for n in range(501)]
    y1 = [ytrans2(model1.model()(empty_moment_kgm + n * dx1)) for n in range(501)]
    ax2.plot([xtrans(x) for x in  x1], y1, 'b')
    ax2.set_xticks([xtrans(0), xtrans(100), xtrans(200), xtrans(300), xtrans(400), xtrans(500)], ['0', '100', '200', '300', '400', '500'])
    ax2.set_yticks([ytrans2(0), ytrans2(100), ytrans2(200)], ['0kg', '100kg', '200kg'])


    ax1.imshow(
        img1, 
        extent=[0, x_extension, 0, ymax1], 
        alpha=0.5,
    )

    model2 = FirstOrderPolynomial(*[[0,0], [1,1]])
    model2.reset_model({'m': 1 / slope_fuel, 't': -inv_model1.model()(pilot_weight_kg + passenger_weight_kg) / slope_fuel})
    inv_model2 = FirstOrderPolynomial(*[[0,0], [1,1]])
    inv_model2.reset_model({'m': slope_fuel, 't': inv_model1.model()(pilot_weight_kg + passenger_weight_kg)})

    dx2 = (inv_model2.model()(fuel_litres) - inv_model1.model()(pilot_weight_kg + passenger_weight_kg)) / 500.0
    x2 = [inv_model1.model()(pilot_weight_kg + passenger_weight_kg) + n * dx2 for n in range(501)]
    y2 = [ytrans1(model2.model()(inv_model1.model()(pilot_weight_kg + passenger_weight_kg) + n * dx2)) for n in range(501)]
    ax1.plot([xtrans(x) for x in  x2], y2, 'b')
    ax1.set_yticks([0, ytrans1(50), ytrans1(100)], ['0l', '50l', '100l'])



    ax3.imshow(
        img3, 
        extent=[0, x_extension, 0, ymax3], 
        alpha=0.5,
    )

    model3 = FirstOrderPolynomial(*[[0,0], [1,1]])
    model3.reset_model({'m': 1 / slope_baggage, 't': -inv_model2.model()(fuel_litres) / slope_baggage})
    inv_model3 = FirstOrderPolynomial(*[[0,0], [1,1]])
    inv_model3.reset_model({'m': slope_baggage, 't': inv_model2.model()(fuel_litres)})

    dx3 = (inv_model3.model()(baggage_weight_kg) - inv_model2.model()(fuel_litres)) / 500.0
    x3 = [inv_model2.model()(fuel_litres) + n * dx3 for n in range(501)]
    y3 = [ytrans3(model3.model()(inv_model2.model()(fuel_litres) + n * dx3)) for n in range(501)]
    ax3.plot([xtrans(x) for x in  x3], y3, 'b')
    ax3.set_yticks([ytrans3(10), ytrans3(30)], ['10kg', '30kg'])



    ax4.imshow(
        img4, 
        extent=[0, x_extension, 0, ymax4], 
        alpha=0.5,
    )

    ax4.set_yticks([ytrans4(400), ytrans4(500), ytrans4(600), ytrans4(700), ytrans4(800)], ['400kg', '500kg', '600kg', '700kg', '800kg'])


    

    x0 = inv_model1.model()(pilot_weight_kg + passenger_weight_kg)
    y0 = ytrans2(model1.model()(x0))

    con = ConnectionPatch(xyA=[xtrans(x0), y0], xyB=[xtrans(x0), 0], coordsA="data", coordsB="data",
    axesA=ax2, axesB=ax1, color="blue", arrowstyle='->')
    ax2.add_artist(con)

    x0 = inv_model2.model()(fuel_litres)
    y0 = ytrans1(model2.model()(inv_model2.model()(fuel_litres)))

    con = ConnectionPatch(xyA=[xtrans(x0), y0], xyB=[xtrans(x0), 0], coordsA="data", coordsB="data",
    axesA=ax1, axesB=ax3, color="blue", arrowstyle='->')
    ax1.add_artist(con)

    x0 = inv_model3.model()(baggage_weight_kg)
    y0 = ytrans3(model3.model()(x0))

    col = 'green' if wb_permissible(aircraft_weight, x0) else 'red'
    con = ConnectionPatch(xyA=[xtrans(x0), y0], xyB=[xtrans(x0), ytrans4(aircraft_weight)], coordsA="data", coordsB="data",
    axesA=ax3, axesB=ax4, color=col, arrowstyle='->')
    ax3.add_artist(con)

    # fig.set_figheight(8)
    fig.savefig(f"{folder}/{filename}.png", dpi=200, bbox_inches='tight')
    # plotter.add_arrow(
    #     x=temp,
    #     y=model_left(temp),
    #     dx=50-temp,
    #     dy=0,
    #     color='red',
    #     x_transform=lambda x: 5*(x+20),
    # )

    # # right hand side plot
    # plotter.plot(
    #     model=model_right,
    #     x0=600,
    #     x1=weight,
    #     x_transform=lambda x: 5*(x-460)/2,
    #     color='r',
    # )
    # plotter.add_arrow(
    #     x=weight,
    #     y=model_right(weight),
    #     dx=780-weight,
    #     dy=0,
    #     color='red',
    #     x_transform=lambda x: 5*(x-460)/2,
    # )

    # # Decorations
    # plotter.add_line(  # separator line (temp / mass)
    #     x0=50,
    #     y0=100,
    #     x1=50,
    #     y1=500,
    #     color='black',
    #     x_transform=lambda x: 5*(x+20),
    # )
    # plotter.add_text_label(  # pressure altitude
    #     x=(temp-20)/2,
    #     y=model_left((temp-20)/2),
    #     text=f"{round(pressure_altitude)} ft",
    #     rotation=math.atan(m/5) / 2.0 / math.pi * 360,
    #     color='red',
    #     x_transform=lambda x: 5*(x+20),
    #     verticalalignment='bottom',
    # )
    # plotter.add_line(  # temperature (line)
    #     x0=temp,
    #     y0=100,
    #     x1=temp,
    #     y1=500,
    #     color='blue',
    #     x_transform=lambda x: 5*(x+20),
    # )
    # plotter.add_text_label(  # temperature (label)
    #     x=temp,
    #     y=505,
    #     text=f"{temp}°C",
    #     color='blue',
    #     x_transform=lambda x: 5*(x+20),
    #     verticalalignment='bottom',
    # )
    # plotter.add_line(  # weight (line)
    #     x0=weight,
    #     y0=100,
    #     x1=weight,
    #     y1=500,
    #     color='blue',
    #     x_transform=lambda x: 5*(x-460)/2,
    # )
    # plotter.add_text_label(  # weight (label)
    #     x=weight,
    #     y=505,
    #     text=f"{weight}kg",
    #     color='blue',
    #     x_transform=lambda x: 5*(x-460)/2,
    #     verticalalignment='bottom',
    # )
    # plotter.add_text_label(  # result
    #     x=810,
    #     y=model_right(weight),
    #     text=f"{round(model_right(weight))}m",
    #     color='red',
    #     horizontalalignment='left',
    # )

    # plotter.save(os.path.join("/code","img", "startroll_0m.png"))