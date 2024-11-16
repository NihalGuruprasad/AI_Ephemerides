import cv2
import numpy as np
from skyfield.api import load
from datetime import datetime
from scipy.optimize import minimize

# Webcam index (set to 2 as specified)
webcam_index = 2

# Define the color range in HSV to detect (example: looking for red color)
lower_color = np.array([0, 100, 100])  # Lower bound of HSV values
upper_color = np.array([10, 255, 255])  # Upper bound of HSV values

# Define the list of coordinates_mercury with assigned numbers
coordinates_mercury = {
    1: [612, 201],
    2: [659, 223],
    3: [686, 261],
    4: [690, 295],
    5: [656, 314],
    6: [596, 310],
    7: [543, 289],
    8: [510, 251],
    9: [527, 216],
    10: [563, 204]
}

# Target coordinates_mercury with associated values
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

# Load ephemeris data from Skyfield (though we're not using it directly here)
ephemeris = load('de440s.bsp')
sun = ephemeris['sun']
mercury = ephemeris['mercury barycenter']  # Direct reference to Mercury's data

# Start capturing from the webcam
webcam = cv2.VideoCapture(webcam_index)

# Check if the webcam is opened successfully
if not webcam.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Skyfield timescale for later use in ephemeris calculations
ts = load.timescale()

def total_distance_mercury(jd, target_value):
    # Define the valid range for Julian dates within the ephemeris
    min_jd = ts.utc(1849, 12, 26).tt
    max_jd = ts.utc(2150, 1, 22).tt

    # Check if jd is within the ephemeris range
    if jd < min_jd or jd > max_jd:
        return 1e10  # Large value to discourage the optimizer from going outside bounds

    t = ts.tt(jd=jd)
    planet_position = mercury.at(t).observe(sun).position.au  # Get position in AU
    
    # Calculate squared distance for this planet from target (using target_value directly)
    distance = sum((planet_position[i] - target_value[i])**2 for i in range(3))
    return distance

while True:
    # Capture a frame from the webcam
    ret, frame = webcam.read()
    if not ret:
        print("Failed to capture image from webcam.")
        break

    # Convert the frame to HSV color space
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Check each numbered coordinate for the specified color
    for coord_num, (x, y) in coordinates_mercury.items():
        # Ensure the coordinate is within frame boundaries
        if y < frame.shape[0] and x < frame.shape[1]:
            # Get the color at the specified coordinate
            pixel_color = hsv_frame[y, x]
            
            # Check if the pixel color is within the target range
            if lower_color[0] <= pixel_color[0] <= upper_color[0] and \
               lower_color[1] <= pixel_color[1] <= upper_color[1] and \
               lower_color[2] <= pixel_color[2] <= upper_color[2]:
                # Draw a circle at the matching point on the frame
                cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)  # Green dot

                # Retrieve the target value from the coordinates_mercury
                target_value = target_coords_mercury.get(str(coord_num))
                
                if target_value:
                    print(f"Coordinate {coord_num} found with color match at ({x}, {y}) -> Target values: {target_value}")
                    
                    # Use the target_value in the ephemeris calculation
                    start_date = datetime(2024, 1, 1)
                    start_jd = ts.utc(start_date.year, start_date.month, start_date.day).tt

                    min_jd = ts.utc(1849, 12, 26).tt
                    max_jd = ts.utc(2150, 1, 22).tt

                    # Perform the ephemeris distance calculation using target_value
                    result = minimize(total_distance_mercury, start_jd, args=(target_value,), bounds=[(min_jd, max_jd)], method='L-BFGS-B')

                    # Convert the result back to a calendar date
                    best_jd = result.x[0]
                    best_date = ts.tt(jd=best_jd).utc_datetime()

                    print(f"Closest matching date for target {coord_num}: {best_date}")
                    
                # Break the loop after the first match (optional)
                break

    # Show the live feed with the marked detected color
    cv2.imshow("Live Feed", frame)

    # Check if 'q' key is pressed to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Exiting the program.")
        break

# Release the webcam and close all windows
webcam.release()
cv2.destroyAllWindows()