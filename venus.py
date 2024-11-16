from skyfield.api import load
from scipy.optimize import minimize
from datetime import datetime

choose_venus = input('? : ')

ephemeris = load('de440s.bsp')
sun = ephemeris['sun']
venus = ephemeris['venus barycenter']  # Direct reference to Mercury's data

target_coords_venus = {

    '1': [-0.7025,0.1490,0.0426],
    '2': [-0.6569,-0.2973,0.0339],
    '3': [-0.3588,-0.6297,0.0121],
    '4': [0.0758,-0.7232,-0.0143],
    '5': [0.4821,-0.5446,-0.0353],
    '6': [0.7077,-0.1619,-0.0431],
    '7': [0.6671,0.2815,-0.0347],
    '8': [0.3733,0.6177,-0.0131],
    '9': [-0.0636,0.7164,0.0135],
    '10': [-0.4756,0.5373,0.0348]
    
}

def total_distance_venus(jd):
    target_key = f'M{choose_venus}'
    # Define the valid range for Julian dates within the ephemeris
    min_jd = ts.utc(1849, 12, 26).tt
    max_jd = ts.utc(2150, 1, 22).tt

    # Check if jd is within the ephemeris range
    if jd < min_jd or jd > max_jd:
        return 1e10  # Large value to discourage the optimizer from going outside bounds

    t = ts.tt(jd=jd)
    planet_position = venus.at(t).observe(sun).position.au  # Get position in AU
    target_position = target_coords_venus[target_key]
    
    # Calculate squared distance for this planet from target
    distance = sum((planet_position[i] - target_position[i])**2 for i in range(3))
    return distance


start_date = datetime(2024, 1, 1)
ts = load.timescale()
start_jd = ts.utc(start_date.year, start_date.month, start_date.day).tt

# Define date boundaries within the ephemeris range (1849–2150)
min_jd = ts.utc(1849, 12, 26).tt
max_jd = ts.utc(2150, 1, 22).tt

# Perform the optimization, using bounds to limit to valid ephemeris range
result = minimize(total_distance_venus, start_jd, bounds=[(min_jd, max_jd)], method='L-BFGS-B')

# Convert the result back to a calendar date
best_jd = result.x[0]
best_date = ts.tt(jd=best_jd).utc_datetime()

print(f"Closest matching date: {best_date}")