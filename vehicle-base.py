# ============================================================
# CONSTANTS
# ============================================================

# --- PID Gains ---
kp = 35
ki = 0.3
kd = 8

# --- Speed ---
base_speed = 80
turn_speed = 60

# --- LiDAR Distances (cm) ---
stop_distance = 5
slow_distance = 10

# --- PID Limits ---
integral_max = 10

# --- Calibration ---
cal_sample_ms = 500
line_threshold = 0.5

# --- Intersection Detection ---
black_threshold = 1200
black_detection_buffer = 1000
at_intersection = False

# ============================================================
# STATE VARIABLES
# ============================================================

# --- Sensor Readings (normalized) ---
left_pos = 0
middle_pos = 0
right_pos = 0

# --- PID State ---
previous_error = 0
previous_nonzero_error = 0
integral = 0

# --- Calibration: Background (dark blue) ---
left_bg = 0
mid_bg = 0
right_bg = 0

# --- Calibration: Blue Line ---
left_line = 0
mid_line = 0
right_line = 0

# --- Calibration: Foreground (white line) ---
left_fg = 0
mid_fg = 0
right_fg = 0

# --- Intersection / Turning ---
turn = 0
last_black_detection = -black_detection_buffer

# ============================================================
# HARDWARE INIT
# ============================================================

matrixLidarDistance.initialize(matrixLidarDistance.Addr.ADDR4, matrixLidarDistance.Matrix.OBS)
maqueenPlusV2.i2c_init()
radio.set_group(37)
maqueenPlusV2.show_color(DigitalPin.P1, maqueenPlusV2.colors(maqueenPlusV2.NeoPixelColors.RED))

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def normalize(raw: number, bg: number, fg: number):
    dif = fg - bg
    if dif == 0:
        return 0
    value = (raw - bg) / dif
    value = min(1, max(0, value))
    return value

def pick_effective_bg(bg_val: number, line_val: number, fg_val: number):
    if abs(fg_val - bg_val) < abs(fg_val - line_val):
        return bg_val
    else:
        return line_val

def wait_for_button_press():
    while not input.button_is_pressed(Button.A):
        basic.pause(20)

def sample_sensors(mode: string):
    global left_bg, mid_bg, right_bg
    global left_line, mid_line, right_line
    global left_fg, mid_fg, right_fg

    left_sum = 0
    mid_sum = 0
    right_sum = 0
    count = 0

    start = input.running_time()
    while input.running_time() - start < cal_sample_ms:
        left_sum += maqueenPlusV2.read_line_sensor_data(maqueenPlusV2.MyEnumLineSensor.SENSOR_L1)
        mid_sum += maqueenPlusV2.read_line_sensor_data(maqueenPlusV2.MyEnumLineSensor.SENSOR_M)
        right_sum += maqueenPlusV2.read_line_sensor_data(maqueenPlusV2.MyEnumLineSensor.SENSOR_R1)
        count += 1
        basic.pause(20)

    if mode == "bg":
        left_bg = left_sum / count
        mid_bg = mid_sum / count
        right_bg = right_sum / count
    elif mode == "line":
        left_line = left_sum / count
        mid_line = mid_sum / count
        right_line = right_sum / count
    else:
        left_fg = left_sum / count
        mid_fg = mid_sum / count
        right_fg = right_sum / count

# ============================================================
# CALIBRATION
# ============================================================

def calibrate_sensors():
    global left_bg, mid_bg, right_bg

    # Phase 1: dark blue background
    basic.show_string("BG")
    wait_for_button_press()
    sample_sensors("bg")
    basic.show_icon(IconNames.YES)
    basic.pause(500)

    # Phase 2: light blue line
    basic.show_string("LINE")
    wait_for_button_press()
    sample_sensors("line")
    basic.show_icon(IconNames.YES)
    basic.pause(500)

    # Phase 3: white line (foreground)
    basic.show_string("FG")
    wait_for_button_press()
    sample_sensors("fg")
    basic.show_icon(IconNames.YES)
    basic.pause(500)

    left_bg = pick_effective_bg(left_bg, left_line, left_fg)
    mid_bg = pick_effective_bg(mid_bg, mid_line, mid_fg)
    right_bg = pick_effective_bg(right_bg, right_line, right_fg)

    basic.clear_screen()

# ============================================================
# LIDAR / SPEED
# ============================================================

def get_target_speed():
    matrixLidarDistance.get_data()
    distance_mm = matrixLidarDistance.get_obstacle_distance(matrixLidarDistance.ObstacleSide.Front)
    distance_cm = distance_mm / 10

    if distance_cm <= stop_distance:
        return 0
    elif distance_cm <= slow_distance:
        return base_speed * ((distance_cm - stop_distance) / (slow_distance - stop_distance))
    else:
        return base_speed

# ============================================================
# LINE FOLLOWING
# ============================================================

def line_follow(speed: number):
    global left_pos, right_pos, middle_pos
    global previous_error, previous_nonzero_error, integral
    global last_black_detection

    left_raw = maqueenPlusV2.read_line_sensor_data(maqueenPlusV2.MyEnumLineSensor.SENSOR_L1)
    right_raw = maqueenPlusV2.read_line_sensor_data(maqueenPlusV2.MyEnumLineSensor.SENSOR_R1)
    middle_raw = maqueenPlusV2.read_line_sensor_data(maqueenPlusV2.MyEnumLineSensor.SENSOR_M)

    if middle_raw < black_threshold \
        or left_raw < black_threshold \
        or right_raw < black_threshold:
        if control.millis() - last_black_detection > black_detection_buffer:
            last_black_detection = control.millis()
            navigate_intersection(speed)
        return

    left_pos = normalize(left_raw, left_bg, left_fg)
    right_pos = normalize(right_raw, right_bg, right_fg)
    middle_pos = normalize(middle_raw, mid_bg, mid_fg)

    # --- Error Calculation ---
    weight_sum = left_pos * -1 + middle_pos * 0 + right_pos * 1
    active_sensors = left_pos + middle_pos + right_pos

    on_left = left_pos > line_threshold
    on_mid = middle_pos > line_threshold
    on_right = right_pos > line_threshold

    if not on_left and not on_mid and not on_right:
        error = 3 if previous_nonzero_error > 0 else -3
        integral = 0
    elif on_left and not on_mid and on_right:
        error = 3 if previous_nonzero_error > 0 else -3
        integral = 0
    else:
        error = weight_sum / active_sensors

    if error != 0:
        previous_nonzero_error = error

    # --- PID Controller ---
    integral = integral + error
    integral = min(integral, integral_max)
    integral = max(-integral_max, integral)

    d = error - previous_error
    correction = kp * error + ki * integral + kd * d
    previous_error = error

    left_speed = speed + correction
    right_speed = speed - correction

    left_speed = min(left_speed, 255)
    left_speed = max(0, left_speed)
    right_speed = min(right_speed, 255)
    right_speed = max(0, right_speed)

    maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.LEFT_MOTOR, maqueenPlusV2.MyEnumDir.FORWARD, left_speed)
    maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.RIGHT_MOTOR, maqueenPlusV2.MyEnumDir.FORWARD, right_speed)

# ============================================================
# INTERSECTION HANDLING
# ============================================================

def navigate_intersection(speed):
    global at_intersection
    maqueenPlusV2.control_motor_stop(maqueenPlusV2.MyEnumMotor.ALL_MOTOR)
    at_intersection = True

def forward(distance, velocity, stop=False):
    maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.ALL_MOTOR, maqueenPlusV2.MyEnumDir.FORWARD, velocity)
    basic.pause(1000 * distance / velocity)
    if stop:
        maqueenPlusV2.control_motor_stop(maqueenPlusV2.MyEnumMotor.ALL_MOTOR)

def turn_left(speed: number):
    maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.RIGHT_MOTOR, maqueenPlusV2.MyEnumDir.FORWARD, speed - 20)
    maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.LEFT_MOTOR, maqueenPlusV2.MyEnumDir.FORWARD, speed + 30)
    basic.pause(2000)
    maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.RIGHT_MOTOR, maqueenPlusV2.MyEnumDir.FORWARD, speed - 40)
    maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.LEFT_MOTOR, maqueenPlusV2.MyEnumDir.FORWARD, speed + 50)
    basic.pause(750)
    maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.ALL_MOTOR, maqueenPlusV2.MyEnumDir.FORWARD, 0)

def turn_right(speed: number):
    maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.LEFT_MOTOR, maqueenPlusV2.MyEnumDir.FORWARD, speed - 20)
    maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.RIGHT_MOTOR, maqueenPlusV2.MyEnumDir.FORWARD, speed + 30)
    basic.pause(2000)
    maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.LEFT_MOTOR, maqueenPlusV2.MyEnumDir.FORWARD, speed - 40)
    maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.RIGHT_MOTOR, maqueenPlusV2.MyEnumDir.FORWARD, speed + 50)
    basic.pause(750)
    maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.ALL_MOTOR, maqueenPlusV2.MyEnumDir.FORWARD, 0)

# ============================================================
# RADIO
# ============================================================

def on_received_number(received_number):
    global turn
    if received_number == 1:
        turn = 1
    elif received_number == 2:
        turn = -1

radio.on_received_number(on_received_number)

# ============================================================
# CALIBRATE ON STARTUP
# ============================================================

calibrate_sensors()

# ============================================================
# MAIN LOOP
# ============================================================

def on_forever():
    global turn, previous_error, integral, at_intersection
    speed = get_target_speed()
    if at_intersection:
        time_intersection = control.millis()
        current_time = 0
        while ((current_time - time_intersection) <= 2500 ):
            if turn != 0:
                if turn == -1:
                    turn_left(speed)
                    break
                if turn == 1:
                    turn_right(speed)
                    break
            current_time = control.millis()
        if turn == 0:
            forward(1, speed, True)
        at_intersection = False
        turn = 0
        previous_error = 0
        integral = 0
    else: 
        line_follow(speed)



basic.forever(on_forever)