from skyfield.api import load
from scipy.optimize import minimize
from datetime import datetime

choose = input('? : ')

ephemeris = load('de440s.bsp')
sun = ephemeris['sun']
uranus = ephemeris['uranus barycenter']  # Direct reference to Mercury's data

target_coords_uranus = {

    '1': [-7.31,16.98,0.23],
    '2': [-16.60,9.15,0.12],
    '3': [-19.36,-2.36,-0.03],
    '4': [-15.04,-13.07,-0.18],
    '5': [-5.53,-19.30,-0.26],
    '6': [5.83,-19.05,-0.26],
    '7': [15.16,-12.26,-0.17],
    '8': [18.92,-1.04,-0.01],
    '9': [15.19,10.53,0.14],
    '10': [5.04,17.59,0.24]
    
}

def total_distance_uranus(jd):
    target_key = f'M{choose}'
    # Define the valid range for Julian dates within the ephemeris
    min_jd = ts.utc(1849, 12, 26).tt
    max_jd = ts.utc(2150, 1, 22).tt

    # Check if jd is within the ephemeris range
    if jd < min_jd or jd > max_jd:
        return 1e10  # Large value to discourage the optimizer from going outside bounds

    t = ts.tt(jd=jd)
    planet_position = uranus.at(t).observe(sun).position.au  # Get position in AU
    target_position = target_coords_uranus[target_key]
    
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
result = minimize(total_distance_uranus, start_jd, bounds=[(min_jd, max_jd)], method='L-BFGS-B')

# Convert the result back to a calendar date
best_jd = result.x[0]
best_date = ts.tt(jd=best_jd).utc_datetime()

print(f"Closest matching date: {best_date}")