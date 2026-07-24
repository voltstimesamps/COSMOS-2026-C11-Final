# Goals:
# - Manage traffic in the city
# - Store rough position of vehicles using the grid
# - Transmit changes in schedule phase

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

# Initialize the last_received number with an invalid
# last_received = -1

# Initalize each position to an invalid position value
positions = [-1,-1,-1,-1]

# Scenario ID
scenario_id = 0

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
    return positions[vehicle_id] >= 0

def get_pos(vehicle_id: int):
    return (get_x(vehicle_id), get_y(vehicle_id))

def get_x(vehicle_id: int):
    return decode_x(positions[vehicle_id])

def get_y(vehicle_id: int):
    return decode_y(positions[vehicle_id])

def store_position(encoded_num: int):
    positions[decode_id(encoded_num)] = decode_pos(encoded_num)

# Radio Functions

def transmit_scenario(scenario_id):
    # Shift scenario ID over 8 bits so they are in correct position for decoding, then send
    radio.send_number(scenario_id << 8) 

def on_received_number(received_number: int):
    if received_number <= 0xff: # 0xff is the value of the highest possible position information
        store_position(received_number)
        update_position_matrix()
    else:
        assert 1==0, "Not yet implemented!" # Guaranteed to raise error in code to terminate program

# Input functions

def on_button_pressed_a():
    global scenario_id

    scenario_id += 1

    transmit_scenario(scenario_id)

# Cosmetic Functions

def update_position_matrix(): # adjust led brightness depending on how many cars are in each cell
    basic.clear_screen()
    for i in range(4):
        if not is_valid_pos(i):
            # Skip execution of loop if there is not valid position data for vehicle with ID i
            continue 

        # Get the last known position of vehicle with ID i
        x, y = get_pos(i) 
        
        # Increase the brightness of LED at position (x,y) by 63
        # Max brightness of 252 when all four cars are in the same cell 
        led.plot_brightness(x, y, led.point_brightness(x,y)+63) 

# Set-up
led.set_display_mode(DisplayMode.GREYSCALE)

radio.set_group(...)

radio.on_received_number(on_received_number)

input.on_button_pressed(Button.A, on_button_pressed_a)

while True:
    # IMPLEMENT FOREVER LOGIC 
    break