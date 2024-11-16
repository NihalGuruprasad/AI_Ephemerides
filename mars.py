from skyfield.api import load
from scipy.optimize import minimize
from datetime import datetime

choose = input('? : ')

ephemeris = load('de440s.bsp')
sun = ephemeris['sun']
mars = ephemeris['mars barycenter']  # Direct reference to Mercury's data

target_coords_mars = {

    '1': [1.0352, 0.9623, 0.0311],
    '2': [0.1948, 1.4787, 0.0478],
    '3': [-0.7359, 1.3965, 0.0451],
    '4': [-1.4190, 0.8276, 0.0267],
    '5': [-1.6660, 0, 0],
    '6': [-1.4190, -0.8276, -0.0267],
    '7': [-0.7359, -1.3965, -0.0451],
    '8': [0.1948, -1.4787, -0.0478],
    '9': [1.0352, -0.9623, -0.0311],
    '10': [1.3814, 0, 0]
    
}

def total_distance_mars(jd):
    target_key = f'M{choose}'
    # Define the valid range for Julian dates within the ephemeris
    min_jd = ts.utc(1849, 12, 26).tt
    max_jd = ts.utc(2150, 1, 22).tt

    # Check if jd is within the ephemeris range
    if jd < min_jd or jd > max_jd:
        return 1e10  # Large value to discourage the optimizer from going outside bounds

    t = ts.tt(jd=jd)
    planet_position = mars.at(t).observe(sun).position.au  # Get position in AU
    target_position = target_coords_mars[target_key]
    
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
result = minimize(total_distance_mars, start_jd, bounds=[(min_jd, max_jd)], method='L-BFGS-B')

# Convert the result back to a calendar date
best_jd = result.x[0]
best_date = ts.tt(jd=best_jd).utc_datetime()

print(f"Closest matching date: {best_date}")