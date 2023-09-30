P0 = 101325  # standard pressure [Pa]
Rs = 287.058  # specific gas constant for dry air [N m/(kg K)]
g = 9.81  # gravitational acceleration on earth's surface [N/kg]
T0 = 288.15  # standard temperature [K]
conv_ft_m = 0.3048

def qnh2qfe(qnh_in_hPa: float, elevation_in_feet: float):
    return ((qnh_in_hPa * 100) - g * P0 / Rs / T0 * elevation_in_feet * conv_ft_m) / 100  # QFE in hPa

def elevation2pressurealtitude(qnh_in_hPa: float, elevation_in_feet: float):
    
    # Exact calculation (to be checked!)
    # qfe = qnh2qfe(qnh_in_hPa=qnh_in_hPa, elevation_in_feet=elevation_in_feet)
    # return (1 - (qfe / P0 * 100)**0.190284) * 145366.45

    # Approximate calculation
    dp = qnh_in_hPa - (P0 / 100)
    return elevation_in_feet - (dp * 27.3)
