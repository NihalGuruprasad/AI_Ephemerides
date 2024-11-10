from skyfield.api import load
from scipy.optimize import minimize
from datetime import datetime

target_coords = []

ephemeris = load('de440s.bsp')

sun = ephemeris['sun']
mercury = ephemeris['mercury barycenter']
venus = ephemeris['venus barycenter']
earth = ephemeris['earth barycenter']
mars = ephemeris['mars barycenter']
jupiter = ephemeris['jupiter barycenter']
saturn = ephemeris['saturn barycenter']
uranus = ephemeris['uranus barycenter']
neptune = ephemeris['neptune barycenter']

choose_mercury = input('Mercury? : ')
choose_venus = input('Venus? : ')
choose_earth = input('Earth? : ')
choose_mars = input('Mars? : ')
choose_jupiter = input('Jupiter? : ')
choose_saturn = input('Saturn? : ')
choose_uranus = input('Uranus? : ')
choose_neptune = input('Neptune? : ')

#######################################################################################

target_coords_mercury = {

    '1': [-0.213, 0.249, 0.040],
    '2': [-0.374, 0.044, 0.038],
    '3': [-0.382, -0.186, 0.020],
    '4': [-0.276, -0.363, -0.004],
    '5': [-0.103, -0.454, -0.028],
    '6': [0.093, -0.444, -0.045],
    '7': [0.266, -0.328, -0.051],
    '8': [0.358, -0.116, -0.042],
    '9': [0.300, 0.136, -0.016],
    '10': [0.068, 0.299, 0.018]
    
}

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

target_coords_earth = {

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

target_coords_jupiter = {

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

###################################################################################################


def total_distance_mercury(jd):
    target_key = f'{choose_mercury}'
    # Define the valid range for Julian dates within the ephemeris
    min_jd = ts.utc(1849, 12, 26).tt
    max_jd = ts.utc(2150, 1, 22).tt

    # Check if jd is within the ephemeris range
    if jd < min_jd or jd > max_jd:
        return 1e10  # Large value to discourage the optimizer from going outside bounds

    t = ts.tt(jd=jd)
    planet_position = mercury.at(t).observe(sun).position.au  # Get position in AU
    target_position = target_coords_mercury[target_key]
    
    # Calculate squared distance for this planet from target
    distance_mercury = sum((planet_position[i] - target_position[i])**2 for i in range(3))

    return distance_mercury

def total_distance_venus(jd):
    target_key = f'{choose_venus}'
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
    distance_venus = sum((planet_position[i] - target_position[i])**2 for i in range(3))
    return distance_venus

def total_distance_earth(jd):
    target_key = f'{choose_earth}'
    # Define the valid range for Julian dates within the ephemeris
    min_jd = ts.utc(1849, 12, 26).tt
    max_jd = ts.utc(2150, 1, 22).tt

    # Check if jd is within the ephemeris range
    if jd < min_jd or jd > max_jd:
        return 1e10  # Large value to discourage the optimizer from going outside bounds

    t = ts.tt(jd=jd)
    planet_position = earth.at(t).observe(sun).position.au  # Get position in AU
    target_position = target_coords_earth[target_key]
    
    # Calculate squared distance for this planet from target
    distance_earth = sum((planet_position[i] - target_position[i])**2 for i in range(3))
    return distance_earth

def total_distance_mars(jd):
    target_key = f'{choose_mars}'
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
    distance_mars = sum((planet_position[i] - target_position[i])**2 for i in range(3))
    return distance_mars

def total_distance_jupiter(jd):
    target_key = f'{choose_jupiter}'
    # Define the valid range for Julian dates within the ephemeris
    min_jd = ts.utc(1849, 12, 26).tt
    max_jd = ts.utc(2150, 1, 22).tt

    # Check if jd is within the ephemeris range
    if jd < min_jd or jd > max_jd:
        return 1e10  # Large value to discourage the optimizer from going outside bounds

    t = ts.tt(jd=jd)
    planet_position = jupiter.at(t).observe(sun).position.au  # Get position in AU
    target_position = target_coords_jupiter[target_key]
    
    # Calculate squared distance for this planet from target
    distance_jupiter = sum((planet_position[i] - target_position[i])**2 for i in range(3))
    return distance_jupiter

def total_distance_saturn(jd):
    target_key = f'{choose_saturn}'
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
    distance_saturn = sum((planet_position[i] - target_position[i])**2 for i in range(3))
    return distance_saturn

def total_distance_uranus(jd):
    target_key = f'{choose_uranus}'
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
    distance_uranus = sum((planet_position[i] - target_position[i])**2 for i in range(3))
    return distance_uranus

def total_distance_neptune(jd):
    target_key = f'{choose_neptune}'
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
    distance_neptune = sum((planet_position[i] - target_position[i])**2 for i in range(3))
    return distance_neptune

def total_distance(jd):

    start_date = datetime(2024, 1, 1)
    ts = load.timescale()
    start_jd = ts.utc(start_date.year, start_date.month, start_date.day).tt
    
    t = ts.tt(jd=jd)
    
    # Calculate squared distances for each planet and sum them
    distance_sum = (
        total_distance_mercury(jd) +
        total_distance_venus(jd) +
        total_distance_earth(jd) +
        total_distance_mars(jd) +
        total_distance_jupiter(jd) +
        total_distance_saturn(jd) +
        total_distance_uranus(jd) +
        total_distance_neptune(jd)
    )
    
    return distance_sum

start_date = datetime(2024, 1, 1)
ts = load.timescale()
start_jd = ts.utc(start_date.year, start_date.month, start_date.day).tt

# Define date boundaries within the ephemeris range (1849–2150)
min_jd = ts.utc(1849, 12, 26).tt
max_jd = ts.utc(2150, 1, 22).tt

# Perform the optimization, using bounds to limit to valid ephemeris range
result = minimize(total_distance, start_jd, bounds=[(min_jd, max_jd)], method='L-BFGS-B')

# Convert the result back to a calendar date
best_jd = result.x[0]
best_date = ts.tt(jd=best_jd).utc_datetime()

print(f"Closest matching date: {best_date}")
