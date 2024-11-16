from skyfield.api import load
from scipy.optimize import minimize
from datetime import datetime

choose = input('? : ')

ephemeris = load('de440s.bsp')
sun = ephemeris['sun']
neptune = ephemeris['neptune barycenter']  # Direct reference to Mercury's data

target_coords_neptune = {

    '1': [-24.93,-16.40,0.91],
    '2': [-10.39,-28.12,0.82],
    '3': [8.16,-29.02,0.41],
    '4': [23.64,-18.92,-0.16],
    '5': [30.27,-1.72,-0.66],
    '6': [25.62,16.12,-0.92],
    '7': [11.38,27.91,-0.84],
    '8': [-7.16,29.12,-0.43],
    '9': [-22.93,19.13,0.13],
    '10': [-29.75,1.69,0.65]
    
}

def total_distance_neptune(jd):
    target_key = f'M{choose}'
    # Define the valid range for Julian dates within the ephemeris
    min_jd = ts.utc(1849, 12, 26).tt
    max_jd = ts.utc(2150, 1, 22).tt

    # Check if jd is within the ephemeris range
    if jd < min_jd or jd > max_jd:
        return 1e10  # Large value to discourage the optimizer from going outside bounds

    t = ts.tt(jd=jd)
    planet_position = neptune.at(t).observe(sun).position.au  # Get position in AU
    target_position = target_coords_neptune[target_key]
    
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
result = minimize(total_distance_neptune, start_jd, bounds=[(min_jd, max_jd)], method='L-BFGS-B')

# Convert the result back to a calendar date
best_jd = result.x[0]
best_date = ts.tt(jd=best_jd).utc_datetime()

print(f"Closest matching date: {best_date}")