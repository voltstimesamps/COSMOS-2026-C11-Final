# Function for detecting vehicles in front of the robot
# Parameter: goal_distance = how far away the robot should stay from the vehicle in front of it
# Outputs modificaitons to speed variable based on distance from vehicle ahead
def vehicle_detection(goal_distance: number):
    global distance, error, base_speed
    min_speed = 0
    proportional_gain = 0.3
    distance = matrixLidarDistance.matrix_point_output(matrixLidarDistance.Addr.ADDR4, 3, 4)
    # Makes sure that it is not reading an object from greater than 80 cm
    if distance <= 0 or distance > 800:
        return base_speed
    error = distance - goal_distance
    # Returns the greatset value between the min speed and the minimum of max speed and attractive potential speed
    return max(min_speed,
        min(max_speed, base_speed + int(proportional_gain * error)))

