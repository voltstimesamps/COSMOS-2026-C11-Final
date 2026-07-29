import Vehicle

# Initialize vehicle object

vehicle = Vehicle.Vehicle(..., ..., ...)

# Return true if vehicle with id vehicle_id is at a valid coordinate
def is_at_valid_pos(vehicle_id: int):
    return vehicle.positions[vehicle_id] >= 0

def get_pos(vehicle_id: int):
    return (get_x(vehicle_id), get_y(vehicle_id))

def get_x(vehicle_id: int):
    return Vehicle.decode_x(vehicle.positions[vehicle_id])

def get_y(vehicle_id: int):
    return Vehicle.decode_y(vehicle.positions[vehicle_id])


# Radio functions 

def on_received_number(received_number: int):
    vehicle.interpret_information(received_number)

# Input functions 

def on_button_pressed_a():
    if vehicle.scenario == 0:
        vehicle.shift_x(1)
        vehicle.show_current_position()
    else:
        maqueenPlusV2.control_motor_stop(maqueenPlusV2.MyEnumMotor.ALL_MOTOR)

def on_button_pressed_b():
    if vehicle.scenario == 0:
        vehicle.shift_y(1)
        vehicle.show_current_position() 
    else:
        pass
        #maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.ALL_MOTOR, maqueenPlusV2.MyEnumDir.FORWARD, NORMAL_SPEED) # speed not final

# Forever loop

def on_forever():
    pass

# Set-up 
radio.on_received_number(on_received_number)

input.on_button_pressed(Button.A, on_button_pressed_a)
input.on_button_pressed(Button.B, on_button_pressed_b)

# Initialize motors
maqueenPlusV2.i2c_init()

# IMPLEMENT PATH FINDING ALGORITHM

# IMPLEMENT CODE SPECIFIC TO EACH VEHICLE

basic.forever(on_forever)
