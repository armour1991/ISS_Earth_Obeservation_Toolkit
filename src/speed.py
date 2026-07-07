def calculate_speed(distance, time_seconds):
    # Calculates speed in m/s

    if time_seconds <= 0:
        raise ValueError("Time difference must be positive.")
    
    return distance / time_seconds