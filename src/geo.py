import math

def calculate_gsd(altitude, fov_deg, image_width):
    #Returns the Ground sampling distance (metres/pixel)

    fov_rad = math.radians(fov_deg)
    ground_width = 2*altitude*math.tan(fov_rad / 2)
    gsd = ground_width / image_width

    return gsd

def pixels_to_distance(pixel_shift, gsd):
    # Converts pixel displacement to ground distance

    return pixel_shift*gsd