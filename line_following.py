# Function for following a line
# Parameters: speed = numerical value 1-255 that controls how fast the robot moves,
# line_brightness = if the line is a "bright" color
# Outputs motor movement for following the line
def line_follow(speed: number, line_brightness: bool):
    # _pos variables all take in signle bit binary values from robot's sensors. 1 is detects line, 0 is does not
    global left_pos, right_pos, middle_pos, far_left_pos, far_right_pos, speed_turn, speed_counter_turn, total_pos
    left_pos = maqueenPlusV2.read_line_sensor_state(maqueenPlusV2.MyEnumLineSensor.SENSOR_L1)
    right_pos = maqueenPlusV2.read_line_sensor_state(maqueenPlusV2.MyEnumLineSensor.SENSOR_R1)
    middle_pos = maqueenPlusV2.read_line_sensor_state(maqueenPlusV2.MyEnumLineSensor.SENSOR_M)
    far_left_pos = maqueenPlusV2.read_line_sensor_state(maqueenPlusV2.MyEnumLineSensor.SENSOR_L2)
    far_right_pos = maqueenPlusV2.read_line_sensor_state(maqueenPlusV2.MyEnumLineSensor.SENSOR_R2)
    # Speed vars for turning. _turn is the wheel going forward, _counter_turn is the wheel going in reverse
    speed_turn = speed + 50
    speed_counter_turn = speed - 40
    total_pos = left_pos + right_pos + middle_pos
    # How many times the robot has attempted reversing
    reverse_counter = 0
    # Line brightness affects the binary values output by the line sensors, and thus the values have to be inverted if the line is a bright color
    if line_brightness == False:
        # If the left sensor is on the line and the right is not, adjust to the right
        if left_pos == 1 and right_pos == 0:
            maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.RIGHT_MOTOR,
                maqueenPlusV2.MyEnumDir.FORWARD,
                speed_turn)
            maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.LEFT_MOTOR,
                maqueenPlusV2.MyEnumDir.FORWARD,
                speed_counter_turn)
        # If the right sensor is on the line and the left is not, adjust to the left
        if right_pos == 1 and left_pos == 0:
            maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.LEFT_MOTOR,
                maqueenPlusV2.MyEnumDir.FORWARD,
                speed_turn)
            maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.RIGHT_MOTOR,
                maqueenPlusV2.MyEnumDir.FORWARD,
                speed_counter_turn)
        # If the middle sensor is on the line, move forward
        if middle_pos == 1:
            maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.LEFT_MOTOR,
                maqueenPlusV2.MyEnumDir.FORWARD,
                speed)
            maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.RIGHT_MOTOR,
                maqueenPlusV2.MyEnumDir.FORWARD,
                speed)
    if line_brightness == True:
        # If the left sensor is on the line and the right is not, adjust to the right
        if left_pos == 0 and right_pos == 1:
            maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.RIGHT_MOTOR,
                maqueenPlusV2.MyEnumDir.FORWARD,
                speed_turn)
            maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.LEFT_MOTOR,
                maqueenPlusV2.MyEnumDir.FORWARD,
                speed_counter_turn)
        # If the right sensor is on the line and the left is not, adjust to the left
        if right_pos == 0 and left_pos == 1:
            maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.LEFT_MOTOR,
                maqueenPlusV2.MyEnumDir.FORWARD,
                speed_turn)
            maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.RIGHT_MOTOR,
                maqueenPlusV2.MyEnumDir.FORWARD,
                speed_counter_turn)
        # If the middle sensor is on the line, move forward
        if middle_pos == 1:
            maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.LEFT_MOTOR,
                maqueenPlusV2.MyEnumDir.FORWARD,
                speed)
            maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.RIGHT_MOTOR,
                maqueenPlusV2.MyEnumDir.FORWARD,
                speed)
    # If more than one sensor is triggered, go backward for 200 ms
    if total_pos >= 2:
        maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.ALL_MOTOR,
            maqueenPlusV2.MyEnumDir.BACKWARD,
            speed)
        reverse_counter += 1
        pause(200)
    # If the robot has reversed five or more times, go backward for 400 ms and reset the reverse counter
    if reverse_counter >= 5:
        maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.ALL_MOTOR,
            maqueenPlusV2.MyEnumDir.BACKWARD,
            speed)
        pause(400)
        reverse_counter = 0
# Initializing variables and init robot
total_pos = 0
speed_counter_turn = 0
speed_turn = 0
far_right_pos = 0
far_left_pos = 0
middle_pos = 0
right_pos = 0
left_pos = 0
maqueenPlusV2.i2c_init()
radio.set_group(37)
