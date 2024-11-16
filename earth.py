from skyfield.api import load
from scipy.optimize import minimize
from datetime import datetime

choose = input('? : ')

ephemeris = load('de440s.bsp')
sun = ephemeris['sun']
earth = ephemeris['earth barycenter']  # Direct reference to Mercury's data

target_coords = {

    '1': [0.7864, 0.5957, 0.0000166],
    '2': [0.2771, 0.9557, 0.0000267],
    '3': [-0.3407, 0.9459, 0.0000264],
    '4': [-0.8314, 0.5798, 0.0000162],
    '5': [-1.0167, 0, 0],
    '6': [-0.8314, -0.5798, -0.0000162],
    '7': [-0.3407, -0.9459, -0.0000264],
    '8': [0.2771, -0.9557, -0.0000267],
    '9': [0.7864, -0.5957, -0.0000166],
    '10': [0.9833, 0, 0]
    
}

def total_distance_earth(jd):
    target_key = f'M{choose}'
    # Define the valid range for Julian dates within the ephemeris
    min_jd = ts.utc(1849, 12, 26).tt
    max_jd = ts.utc(2150, 1, 22).tt

    # Check if jd is within the ephemeris range
    if jd < min_jd or jd > max_jd:
        return 1e10  # Large value to discourage the optimizer from going outside bounds

    t = ts.tt(jd=jd)
    planet_position = earth.at(t).observe(sun).position.au  # Get position in AU
    target_position = target_coords[target_key]
    
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
result = minimize(total_distance_earth, start_jd, bounds=[(min_jd, max_jd)], method='L-BFGS-B')

# Convert the result back to a calendar date
best_jd = result.x[0]
best_date = ts.tt(jd=best_jd).utc_datetime()

print(f"Closest matching date: {best_date}")