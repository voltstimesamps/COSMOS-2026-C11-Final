# Variables
Kp = 40
Kd = 20
previous_error = 0
speed_turn = 0
middle_pos = 0
right_pos = 0
left_pos = 0
far_right_pos = 0
far_left_pos = 0

# Init
maqueenPlusV2.i2c_init()
radio.set_group(37)