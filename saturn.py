from skyfield.api import load
from scipy.optimize import minimize
from datetime import datetime

choose = input('? : ')

ephemeris = load('de440s.bsp')
sun = ephemeris['sun']
saturn = ephemeris['saturn barycenter']  # Direct reference to Mercury's data

target_coords_saturn = {

    '1': [-8.21,4.07,0.18],
    '2': [-9.24,-1.94,-0.08],
    '3': [-6.59,-7.21,-0.31],
    '4': [-1.53,-9.90,-0.43],
    '5': [4.06,-9.26,-0.40],
    '6': [8.32,-5.58,-0.24],
    '7': [9.77,-0.04,-0.002],
    '8': [7.69,5.48,0.24],
    '9': [2.57,8.79,0.38],
    '10': [-3.63,8.28,0.36]
    
}

def total_distance_saturn(jd):
    target_key = f'M{choose}'
    # Define the valid range for Julian dates within the ephemeris
    min_jd = ts.utc(1849, 12, 26).tt
    max_jd = ts.utc(2150, 1, 22).tt

    # Check if jd is within the ephemeris range
    if jd < min_jd or jd > max_jd:
        return 1e10  # Large value to discourage the optimizer from going outside bounds

    t = ts.tt(jd=jd)
    planet_position = saturn.at(t).observe(sun).position.au  # Get position in AU
    target_position = target_coords_saturn[target_key]
    
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
result = minimize(total_distance_saturn, start_jd, bounds=[(min_jd, max_jd)], method='L-BFGS-B')

# Convert the result back to a calendar date
best_jd = result.x[0]
best_date = ts.tt(jd=best_jd).utc_datetime()

print(f"Closest matching date: {best_date}")