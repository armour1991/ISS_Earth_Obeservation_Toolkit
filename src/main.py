from config import *
from image_utils import *
from geo import *

img1, img2, gray1, gray2 = load_images(
    "C:/Amritbir_1024150159/ISS Earth Observation Toolkit/Data/raw_images/image1.jpg",
    "C:/Amritbir_1024150159/ISS Earth Observation Toolkit/Data/raw_images/image2.jpg"
)

kp1, des1, kp2, des2 = detect_features(
    gray1,
    gray2
)

matches, matched_image = match_features(
    img1,
    img2,
    kp1,
    kp2,
    des1,
    des2
)

display_matches(matched_image)

pixel_shift, M = calculate_pixel_shift(
    kp1,
    kp2,
    matches
)

print(f"Pixel Shift: {pixel_shift:.2f} pixels")
print(M)

gsd = calculate_gsd(
    ISS_ALTITUDE,
    CAMERA_FOV,
    IMAGE_WIDTH
)

ground_distance = pixels_to_distance(
    pixel_shift,
    gsd
)

print(f"GSD = {gsd:.2f} m/pixel")
print(f"Ground Distance: {ground_distance:.2f} metres")
