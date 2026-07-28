# Constants
Kp = 40
Kd = 20

previous_error = 0

def line_follow(speed: number, line_brightness: bool):
    global left_pos, right_pos, middle_pos, far_left_pos, far_right_pos
    global previous_error

    # Read sensors
    left_pos = maqueenPlusV2.read_line_sensor_state(maqueenPlusV2.MyEnumLineSensor.SENSOR_L1)
    right_pos = maqueenPlusV2.read_line_sensor_state(maqueenPlusV2.MyEnumLineSensor.SENSOR_R1)
    middle_pos = maqueenPlusV2.read_line_sensor_state(maqueenPlusV2.MyEnumLineSensor.SENSOR_M)
    #far_left_pos = maqueenPlusV2.read_line_sensor_state(maqueenPlusV2.MyEnumLineSensor.SENSOR_L2)
    #far_right_pos = maqueenPlusV2.read_line_sensor_state(maqueenPlusV2.MyEnumLineSensor.SENSOR_R2)

    if line_brightness:
        left_pos = 1 - left_pos
        right_pos = 1 - right_pos
        middle_pos = 1 - middle_pos
        far_left_pos = 1 - far_left_pos
        far_right_pos = 1 - far_right_pos

    # --- ERROR CALCULATION ---
    
    # 010:On line
    if left_pos == 0 and middle_pos == 1 and right_pos == 0:
        error = 0

    # 110: Left
    elif left_pos == 1 and middle_pos == 1 and right_pos == 0:
        error = -1

    # 100: Far Left
    elif left_pos == 1 and middle_pos == 0 and right_pos == 0:
        error = -2

    # 011: Right
    elif left_pos == 0 and middle_pos == 1 and right_pos == 1:
        error = 1

    # 001: Far right
    elif left_pos == 0 and middle_pos == 0 and right_pos == 1:
        error = 2

    #111: On Line
    elif left_pos == 1 and middle_pos == 1 and right_pos == 1:
        error = 0

    #Edge Cases
    elif left_pos == 1 and middle_pos == 0 and right_pos == 1:
        error = previous_error

    elif left_pos == 0 and middle_pos == 0 and right_pos == 0:
        error = 2 * previous_error #??

    # --- PD CONTROLLER ---

    d = error - previous_error
    correction = Kp * error + Kd * d
    previous_error = error

    left_speed = speed + correction
    right_speed = speed - correction

    # Set speed between 0-255
    left_speed = min(left_speed, 255)
    left_speed = max(0, left_speed)
    right_speed = min(right_speed, 255)
    right_speed = max(0, right_speed)

    maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.LEFT_MOTOR, maqueenPlusV2.MyEnumDir.FORWARD, left_speed)
    maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.RIGHT_MOTOR, maqueenPlusV2.MyEnumDir.FORWARD, right_speed)
    
# Init
speed_turn = 0
middle_pos = 0
right_pos = 0
left_pos = 0

far_right_pos = 0
far_left_pos = 0

maqueenPlusV2.i2c_init()
radio.set_group(37)

# Loop
def on_forever():
    line_follow(100, False)

basic.forever(on_forever)
