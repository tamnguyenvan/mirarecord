from sys import argv
import cv2
import numpy as np

# Easing function for smooth zooming
def ease_in_out_quad(t):
    return t*t*(3 - 2*t) if t < 0.5 else 1 - (t-0.5)*(t-0.5)*2

# Function to calculate zoom parameters
def calculate_zoom_parameters(zoom_center, base_zoom_factor, start_time, duration, timestamp):
    # Calculate elapsed time since the start of zoom
    elapsed_time = timestamp - start_time

    # Calculate the progress of zooming from 0 to 1
    progress = min(elapsed_time / duration, 1.0)

    # Apply easing function to smooth the progress
    progress = ease_in_out_quad(progress)

    if progress <= 0.5:
        # Zoom in during the first half
        current_factor = 1.0 + (base_zoom_factor - 1.0) * (2 * progress)
    else:
        # Zoom out during the second half
        current_factor = base_zoom_factor - (base_zoom_factor - 1.0) * (2 * (progress - 0.5))

    # Calculate the zoomed width and height
    zoomed_width = int(width / current_factor)
    zoomed_height = int(height / current_factor)

    # Calculate the crop region around the zoom center
    x = max(0, zoom_center[0] - zoomed_width // 2)
    y = max(0, zoom_center[1] - zoomed_height // 2)

    return current_factor, (x, y, zoomed_width, zoomed_height)

# Open the video file
video_path = argv[1]
cap = cv2.VideoCapture(video_path)

# Check if the video opened successfully
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# Specify zoom parameters (center point, zoom factor, start time, duration in seconds)
zoom_center = (1900, 10)  # Zoom center (x, y)
base_zoom_factor = 2.0     # Final zoom factor
start_time = 3             # Start time of zoom effect in seconds
duration =  1.8              # Duration of zoom effect in seconds

# Read the first frame to get the video dimensions
ret, frame = cap.read()
if not ret:
    print("Error: Could not read first frame.")
    exit()
height, width = frame.shape[:2]

# Process each frame
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        break

    # Calculate timestamp
    timestamp = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000  # Convert milliseconds to seconds

    # Calculate zoom parameters at the current timestamp
    if timestamp >= start_time:
        zoom_factor, crop_params = calculate_zoom_parameters(zoom_center, base_zoom_factor, start_time, duration, timestamp)
    else:
        zoom_factor = 1.0  # No zoom effect before the start time
        crop_params = (0, 0, width, height)  # Full frame

    # Crop the zoomed region
    x, y, zoomed_width, zoomed_height = crop_params
    zoomed_region = frame[y:y+zoomed_height, x:x+zoomed_width]

    # Resize the cropped region to the original size with cubic interpolation
    zoomed_frame = cv2.resize(zoomed_region, (width, height), interpolation=cv2.INTER_CUBIC)

    # Display the zoomed frame
    cv2.imshow('Zoomed Video', zoomed_frame)

    # Exit if 'q' is pressed
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()
