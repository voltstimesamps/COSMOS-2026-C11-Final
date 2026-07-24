# Goals:
# - Manage traffic in the city
# - Store rough position of vehicles using the grid
# - Transmit changes in schedule phase

# bitwise AND-ing these masks and the number that encodes each 
# vehicle's position then shifting the resulting number will 
# yield different information from each part of the number 

ID_MASK = 0b11000000
POS_MASK = 0b111111
X_MASK = 0b111000
Y_MASK = 0b111

# Initialize the last_received number with an invalid
last_received = -1

# Initalize each position to an invalid position value
positions = [-1,-1,-1,-1] 

def decode_id(encoded_num: int):
    return (ID_MASK & encoded_num) >> 6

def decode_pos(encoded_num: int):
    return POS_MASK & encoded_num

def decode_x(encoded_num: int):
    return (X_MASK & encoded_num) >> 3

def decode_y(encoded_num: int):
    return (Y_MASK & encoded_num)

def get_pos(vehicle_id: int):
    return get_x(vehicle_id), get_y(vehicle_id)

def get_x(vehicle_id: int):
    return decode_x(positions[vehicle_id])

def get_y(vehicle_id: int):
    return decode_y(positions[vehicle_id])

def store_position(encoded_num: int):
    positions[decode_id(encoded_num)] = decode_pos(encoded_num)

def on_received_number(received_number: int):
    if received_number <= 0xff: # 0xff is the value of the highest possible position information
        store_position(received_number)
        update_led()
    else:
        raise NotImplementedError

def update_led(): # adjust led brightness depending on how many cars are in each cell
    for i in range(4):
        pos = get_pos(i)
        led.plot_brightness(*pos, led.point_brightness(*pos)+63)

radio.set_group(...)

while True:
    radio.on_received_number(on_received_number)
    ...