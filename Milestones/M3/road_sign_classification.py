BASE_SPEED = 40
MIN_CONTINUOUS_SIGNAL_FOR_CHANGE = 2

speed_mult = 1.0
last_signal_class = -1
continuous_signal_count = 0

# Initialize components (Motors and Huskylens)
maqueenPlusV2.i2c_init() # Connect to motors
huskylens.init_i2c() # Connect to Huskylens
huskylens.init_mode(protocolAlgorithm.OBJECTCLASSIFICATION) # Set to classify

# Movement function
def set_motor_speeds(left, right):
    maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.LEFT_MOTOR, maqueenPlusV2.MyEnumDir.FORWARD, left)
    maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.RIGHT_MOTOR, maqueenPlusV2.MyEnumDir.Forward, right)

def get_time_to_stop(current_speed):
    C = 40000 # C found through trial and error
    return C // current_speed

# Check
def huskylens_integration():
    global speed_mult
    global last_signal_class
    global continuous_signal_count
    
    # Get data
    huskylens.request()

    # 1 is nothing; 2 is stop sign; 3 is SL=35; 4 is SL=45; 5 is SL=25
    detection_class = huskylens.readBox_s(Content3.ID)
    
    # # Display on screen for debugging
    # basic.show_number(detection_class)

    # Reset signal count if the signal changed
    if last_signal_class != detection_class:
        last_signal_class = detection_class
        continuous_signal_count = 0
    continuous_signal_count += 1
    
    # Don't change anything if signal count is too low
    if continuous_signal_count < MIN_CONTINUOUS_SIGNAL_FOR_CHANGE:
        return
    
    # If signal count is sufficient, then change accordingly
    if detection_class == 2: # STOP SIGN
        stop_in = get_time_to_stop(BASE_SPEED * speed_mult)
        basic.pause(stop_in)
        set_motor_speeds(0,0)
        basic.pause(3000) # 3 second pause
    elif detection_class == 3: # SL 35
        speed_mult = 1.4
    elif detection_class == 4: # SL 45
        speed_mult = 1.8
    elif detection_class == 5: # SL 25
        speed_mult = 1.0
    continuous_signal_count = 0

    # Conduct the change
    set_motor_speeds(BASE_SPEED * speed_mult,BASE_SPEED * speed_mult)

basic.forever(huskylens_integration)
