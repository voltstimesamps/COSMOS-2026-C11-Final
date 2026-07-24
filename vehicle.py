# Goals:
# - Store vehicle name (optional)
# - Store vehicle id
# - Store position
# - Initalize Radio
# - Transmit position
# - Run small pathfinding algorithm that avoids other vehicles
# - Low priority: have a themed face on each vehicle after scenario 0 is over

class Vehicle:
    def __init__(self,  vehicle_id: int, name:str, radio_channel: int=37):
        radio.set_group(radio_channel)
        # police =      0b00 = 0
        # ambulance =   0b01 = 1
        # drunk =       0b10 = 2
        # good =        0b11 = 3
        self.name = name
        self.vehicle_id = vehicle_id

        # Initalize positions with invalid position values
        # Only other vehicles positions will be stored
        self.positions = [-1,-1,-1,-1] 
        
        #   0 1 2 3 4
        # 0 @ @ @ @ @
        # 1 @   @   @
        # 2 @ @ @ @ @
        # 3 @   @   @
        # 4 @ @ @ @ @

        self.x_pos = 0 # Value between 0 and 4 (0b100) based on map above
        self.y_pos = 0 # Value between 0 and 4 (0b100) based on map above
        self.show_stored_position()
        self.transmit_position()

        self.scenario = 0

    def update_channel(self, radio_channel: int):
        radio.set_group(radio_channel)

    def set_x(self, x_new): # Set internal x_pos to new x_pos
        self.x_pos = x_new
        self.transmit_position()
                
    def shift_x(self, dx):
        self.x_pos += dx # Shift inter x_pos by dx
        self.x_pos %= 5
        self.transmit_position()
        
    def set_y(self, y_new): # Set internal y_pos to new y_pos
        self.y_pos = y_new
        self.transmit_position()
        
    def shift_y(self, dy):
        self.y_pos += dy # Shift inter x_pos by dx
        self.y_pos %= 5
        self.transmit_position()

    def transmit_position(self):
        # bits 7, 6 for vehicle id (4 possible IDs)
        # bits 5, 4, 3 for x position (5 possible positions)
        # bits 2, 1, 0 for y position (5 possible positions)
        send_num = self.vehicle_id
        send_num <<= 3
        send_num += self.x_pos
        send_num <<= 3
        send_num += self.y_pos
        radio.send_number(send_num)

    def store_position(self, encoded_num: int):
        self.positions[decode_id(encoded_num)] = decode_pos(encoded_num)

    def show_stored_position(self):
        basic.clear_screen()
        led.plot(self.x_pos,self.y_pos)

    def update_position_matrix(self): # adjust led brightness depending on how many cars are in each cell
        basic.clear_screen()
        for i in range(4):
            if not is_valid_pos(i): 
                led.plot(self.x_pos, self.y_pos)
                # Skip execution of loop if there is not valid position data for vehicle with ID i
                continue 

            # Get the last known position of vehicle with ID i
            x, y = get_pos(i) 
            
            # Increase the brightness of LED at position (x,y) by 63
            # Max brightness of 252 when all four cars are in the same cell 
            led.plot_brightness(x, y, led.point_brightness(x,y)+63) 

    

# Initialize vehicle object
vehicle = Vehicle(..., ..., ...)

# Constants
# Constant speeds depending on road signage, heavily subject to change
SLOW_SPEED = 10 
# Constant speeds depending on road signage, heavily subject to change
NORMAL_SPEED = 100 
# Constant speeds depending on road signage, heavily subject to change
FAST_SPEED = 255 


# bitwise AND-ing this masks and the number that encodes info about the
# traffic situation then shifting the resulting number will
# yield different information from each part of the number

# First 4 bits are for scenario ID
# Next 2 bits are for vehicle ID
# Next 3 bits are for X position
# Next 3 bits are for Y position
SCENARIO_MASK = 0b111100000000
ID_MASK = 0b11000000
POS_MASK = 0b111111
X_MASK = 0b111000
Y_MASK = 0b111

# Decode functions

def decode_scenario(encoded_num: int):
    return (SCENARIO_MASK & encoded_num) >> 8

def decode_id(encoded_num: int):
    return (ID_MASK & encoded_num) >> 6

def decode_pos(encoded_num: int):
    return POS_MASK & encoded_num

def decode_x(encoded_num: int):
    return (X_MASK & encoded_num) >> 3

def decode_y(encoded_num: int):
    return (Y_MASK & encoded_num)

# Access functions

def is_valid_pos(vehicle_id: int):
    return vehicle.positions[vehicle_id] >= 0

def get_pos(vehicle_id: int):
    return (get_x(vehicle_id), get_y(vehicle_id))

def get_x(vehicle_id: int):
    return decode_x(vehicle.positions[vehicle_id])

def get_y(vehicle_id: int):
    return decode_y(vehicle.positions[vehicle_id])

# Radio functions 

def on_received_number(received_number: int):
    vehicle.scenario = decode_scenario(received_number)
    vehicle.store_position(received_number)

# Input functions 

def on_button_pressed_a():
    if vehicle.scenario == 0:
        vehicle.shift_x(1)
        vehicle.show_stored_position()
    else:
        maqueenPlusV2.control_motor_stop(maqueenPlusV2.MyEnumMotor.ALL_MOTOR)

def on_button_pressed_b():
    if vehicle.scenario == 0:
        vehicle.shift_y(1)
        vehicle.show_stored_position() 
    else:
        maqueenPlusV2.control_motor(maqueenPlusV2.MyEnumMotor.ALL_MOTOR, maqueenPlusV2.MyEnumDir.FORWARD, NORMAL_SPEED) # speed not final

# Set-up 
led.set_display_mode(DisplayMode.GREYSCALE)

radio.on_received_number(on_received_number)

input.on_button_pressed(Button.A, on_button_pressed_a)
input.on_button_pressed(Button.B, on_button_pressed_b)

# Initialize motors
maqueenPlusV2.i2c_init()

# IMPLEMENT PATH FINDING ALGORITHMs

# IMPLEMENT CODE SPECIFIC TO EACH VEHICLE

while True:
    # IMPLEMENT LOGIC PER VEHICLE
    break