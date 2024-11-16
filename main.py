import numpy as np
from skyfield.api import load
from datetime import datetime
from scipy.optimize import differential_evolution, minimize
from PIL import Image
from functools import partial


def is_grey_or_black(r, g, b, grey_tolerance=60):
    if r == 0 and g == 0 and b == 0:  # Black
        return True
    return abs(r - g) <= grey_tolerance and abs(g - b) <= grey_tolerance and abs(r - b) <= grey_tolerance


def find_non_grey_or_black_coordinates(image_path, coordinates):
    image = Image.open(image_path)
    pixels = image.load()
    non_grey_coordinates = [
        coord for coord in coordinates
        if not is_grey_or_black(*pixels[coord[0], coord[1]])
    ]
    return non_grey_coordinates


ephemeris = load('de440.bsp')
sun = ephemeris['sun']
planets = {
    'mercury': ephemeris['mercury barycenter'],
    'venus': ephemeris['venus barycenter'],
    'earth': ephemeris['earth barycenter'],
    'mars': ephemeris['mars barycenter'],
    'jupiter': ephemeris['jupiter barycenter'],
    'saturn': ephemeris['saturn barycenter'],
    'uranus': ephemeris['uranus barycenter'],
    'neptune': ephemeris['neptune barycenter']
}
ts = load.timescale()


def total_distance(jd, target_coords):
    t = ts.tt(jd=jd[0])
    total_dist = 0

    for planet_name, target_value in target_coords.items():
        planet_position = planets[planet_name].at(t).observe(sun).position.au
        distance = np.linalg.norm(planet_position - target_value)
        total_dist += distance
        # print(f"{planet_name} | Observed: {planet_position} | Target: {target_value} | Distance: {distance}")

    # print(f"Total Distance for JD {jd[0]}: {total_dist}")
    return total_dist


image_path = "image.jpg"  
coordinates_to_target = {
    (530, 235): [0.268, 0.217, 0.023], (497, 216): [0.086, 0.386, -0.004], (517, 184): [-0.132, 0.416, -0.031], (565, 160): [-0.316, 0.333, -0.049], (623, 152): [-0.428, 0.173, -0.057], (693, 164): [-0.444, -0.026, -0.051], (725, 186): [-0.347, -0.216, -0.033], (721, 217): [-0.139, -0.333, -0.004], (653, 241): [0.127, -0.29, 0.026], (591, 254): [0.302, -0.06, 0.038],
    (676, 260): [0.619, 0.372, -0.021], (565, 272): [0.284, 0.666, -0.039], (490, 255): [-0.159, 0.709, -0.042], (450, 215): [-0.543, 0.485, -0.03], (472, 173): [-0.723, 0.079, -0.006], (533, 142): [-0.631, -0.356, 0.02], (647, 135): [-0.299, -0.656, 0.038], (736, 147): [0.148, -0.703, 0.042], (781, 185): [0.537, -0.477, 0.029], (762, 234): [0.717, -0.065, 0.005],
    (748, 122): [-0.902, -0.391, 0.0], (837, 165): [-0.485, -0.859, 0.0], (823, 231): [0.125, -0.987, 0.0], (726, 288): [0.688, -0.733, -0.0], (580, 313): [0.993, -0.202, -0.0], (442, 291): [0.933, 0.404, -0.0], (383, 237): [0.533, 0.862, -0.0], (410, 174): [-0.063, 1.003, -0.0], (517, 124): [-0.634, 0.767, 0.0], (641, 113): [-0.958, 0.234, 0.0],
    (690, 84): [1.249, 0.716, 0.026], (819, 113): [0.577, 1.412, 0.047], (883, 153): [-0.324, 1.573, 0.05], (873, 267): [-1.125, 1.216, 0.036], (715, 331): [-1.588, 0.491, 0.012], (492, 341): [-1.578, -0.379, -0.016], (377, 298): [-1.064, -1.123, -0.039], (338, 226): [-0.168, -1.449, -0.047], (393, 147): [0.79, -1.149, -0.035], (517, 100): [1.355, -0.291, -0.006],
    (317, 323): [-4.766, 2.223, 0.103], (252, 243): [-5.32, -0.867, 0.052], (313, 156): [-4.034, -3.668, -0.017], (487, 85): [-1.397, -5.243, -0.081], (684, 67): [1.708, -5.038, -0.117], (855, 90): [4.186, -3.03, -0.111], (967, 159): [5.024, 0.142, -0.062], (969, 262): [3.748, 3.238, 0.013], (793, 356): [0.833, 4.914, 0.082], (501, 393): [-2.453, 4.475, 0.116],
    (201, 307): [-1.411, -9.66, -0.223], (220, 197): [4.239, -9.034, -0.393], (356, 99): [8.481, -5.371, -0.432], (557, 52): [9.926, 0.059, -0.328], (769, 48): [7.99, 5.45, -0.113], (955, 93): [3.138, 8.811, 0.142], (1060, 180): [-2.944, 8.605, 0.338], (998, 327): [-7.719, 4.661, 0.387], (692, 433): [-9.06, -1.363, 0.263], (377, 418): [-6.528, -6.838, 0.026],
    (174, 398): [-17.405, -7.565, -0.241], (130, 259): [-10.005, -16.778, -0.253], (243, 127): [1.078, -19.924, -0.173], (456, 49): [11.82, -16.251, -0.034], (654, 27): [18.598, -7.131, 0.117], (907, 47): [18.97, 4.411, 0.227], (1085, 115): [12.404, 14.281, 0.254], (1144, 275): [0.956, 18.426, 0.18], (930, 428): [-10.853, 14.713, 0.029], (497, 498): [-17.919, 4.567, -0.134],
    (1261, 219): [-16.187, 25.547, 0.041], (1115, 435): [-28.075, 11.444, -0.509], (600, 574): [-29.491, -6.931, -0.87], (136, 489): [-19.889, -22.71, -0.906], (18, 310): [-2.795, -29.91, -0.599], (128, 147): [15.351, -25.658, -0.064], (361, 50): [27.525, -11.454, 0.495], (627, 4): [28.933, 7.225, 0.861], (896, 23): [19.04, 23.091, 0.891], (1116, 83): [1.774, 30.04, 0.576]
}


coordinates = list(coordinates_to_target.keys())
non_grey_coordinates = find_non_grey_or_black_coordinates(image_path, coordinates)


user_coords = {
    planet_name: coordinates_to_target[coord]
    for planet_name, coord in zip(planets.keys(), non_grey_coordinates)
    if coord in coordinates_to_target
}


min_jd = ts.utc(1849, 12, 26).tt
max_jd = ts.utc(2150, 1, 22).tt
bounds = [(min_jd, max_jd)]

# t = ts.utc(2000, 1, 1)
# for planet_name, planet in planets.items():
#     print(f"{planet_name}: {planet.at(t).observe(sun).position.au}")


result = differential_evolution(
    func=partial(total_distance, target_coords=user_coords),
    bounds=bounds,
    strategy='best1bin',
    maxiter=5000,
    popsize=100,
    tol=1e-8,
    disp=True,
    seed=42
)


result_local = minimize(
    total_distance,
    x0=result.x,
    args=(user_coords,),
    method='L-BFGS-B',
    bounds=bounds
)

best_jd = result_local.x[0]
best_date = ts.tt(jd=best_jd).utc_datetime()
print(f"Final closest matching date: {best_date}")