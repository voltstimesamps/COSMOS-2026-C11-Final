# Function for detecting vehicles in front of the robot
# Parameter: goal_distance = how far away the robot should stay from the vehicle in front of it
# Outputs modificaitons to speed variable based on distance from vehicle ahead
def vehicle_detection(goal_distance):
    global middle_matrix_distance, reduction_counter, speed
    # The distance from the middle of the matrix defined in mm
    middle_matrix_distance = matrixLidarDistance.matrix_point_output(matrixLidarDistance.Addr.ADDR4, 4, 4)
    goal_distance = 200
    # While the goal distance does not equal the matrix distance,
    # If the matrix distance is less than the goal distance reduce the speed by ten,
    # and if the matrix distance is greater than the goal distance, increase the speed by ten
    while (goal_distance != middle_matrix_distance):
        if (middle_matrix_distance < goal_distance):
            speed += -10
        if (middle_matrix_distance > goal_distance):
            speed += 10
    return speed

# Variable definition and init
middle_matrix_distance = 0
reduction_counter = 0
maqueenPlusV2.i2c_init()
radio.set_group(37)
matrixLidarDistance.initialize(matrixLidarDistance.Addr.ADDR4,
    matrixLidarDistance.Matrix.MAT)

