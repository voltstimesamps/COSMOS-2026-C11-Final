# Goals:
# - Store vehicle name (optional)
# - Store vehicle id
# - Store position
# - Initalize Radio
# - Transmit position
# - Run small pathfinding algorithm that avoids other vehicles
# - Low priority: have a themed face on each vehicle after scenario 0 is over

class Vehicle:
    def __init__(self, vehicle_id: int, name: str, black_threshold: int, x_initial: int, y_initial: int, radio_channel: int=37):
        radio.set_group(radio_channel)
        # police =      0b00 = 0
        # ambulance =   0b01 = 1
        # drunk =       0b10 = 2
        # good =        0b11 = 3
        self.name = name
        self.vehicle_id = vehicle_id
        self.black_threshold = black_threshold
        # Initalize positions with invalid position values
        # Only other vehicles positions will be stored
        self.positions = [-1,-1,-1,-1] 
        
        #   0 1 2 3 4
        # 0 @ @ @ @ @
        # 1 @   @   @
        # 2 @ @ @ @ @
        # 3 @   @   @
        # 4 @ @ @ @ @

        self.vehicle_map = self.gen_blank_5x5()

        self.x_pos = x_initial # Value between 0 and 4 (0b100) based on map above
        self.y_pos = y_initial # Value between 0 and 4 (0b100) based on map above
        self.show_current_position()
        self.transmit_position()
        
        self.scenario = 0

    def gen_blank_5x5(self):
        out = []
        for x in range(5):
            column = []
            for y in range(5):
                column.append(0)
            out.append(column)
        return out
    
    def show_current_position(self):
        basic.clear_screen()
        led.plot(self.x_pos,self.y_pos)

    def set_x(self, x_new): # Set internal x_pos to new x_pos
        self.x_pos = x_new
        self.transmit_position()
                
    def shift_x(self, dx):
        self.x_pos += dx # Shift internal x_pos by dx
        self.x_pos %= 5
        self.transmit_position()
        
    def set_y(self, y_new): # Set internal y_pos to new y_pos
        self.y_pos = y_new
        self.transmit_position()
        
    def shift_y(self, dy):
        self.y_pos += dy # Shift internal y_pos by dy
        self.y_pos %= 5
        self.transmit_position()

    # Receive functions

    def interpret_information(self, encoded_num:int):
        self.store_position(encoded_num)

        scenario = decode_scenario(encoded_num)
        # If received scenario is a valid scenario, set the scenario
        if 0 <= scenario < 0xe:  
            self.scenario = scenario
        else:
            if scenario == 0xe or self.vehicle_id == decode_id(encoded_num): 
                self.execute_action(decode_action(encoded_num))

    def at(self, x, y): # Returns true if this Vehicle is at (x,y)
        return self.x_pos == x and self.y_pos == y

    def store_position(self, encoded_num: int):
        pos = decode_pos(encoded_num)
        self.positions[decode_id(encoded_num)] = pos
        self.update_position_array()

    def update_position_array(self):
        self.vehicle_map = self.gen_blank_5x5()
        for pos in self.positions:
            if pos == -1:
                continue
            x, y = decode_x(pos), decode_y(pos)
            self.vehicle_map[x][y]

    def interpret_tape(self, junction_action:int=-1):
        x = self.x_pos
        y = self.y_pos
        if junction_action == -1:
            if self.at(0,0) or self.at(1,0) or self.at(3,0) \
                or self.at(1,2) or self.at(1,2):
                x += 1
            elif self.at(4,0) or self.at(4,0) or self.at(4,0)\
                or self.at(2,1) or self.at(2,3):
                y += 1
            elif self.at(4,4) or self.at(3,4) or self.at(1,4):
                x -= 1
            elif self.at(0,4) or self.at(0,3) or self.at(0,1):
                y -= 1
        elif junction_action == 0: # Straightaway
            if self.at(0,3):
                y-=2
            elif self.at(1,0):
                x+=2
            elif self.at(4,1):
                y+=2
            elif self.at(3,4):
                x-=2
        elif junction_action == 1: # forward->right
            if self.at(0,3):
                y-=1
                x+=1
            elif self.at(2,3):
                y+=1
                x-=1
            elif self.at(1,0) or self.at(1,2) or self.at(3,2):
                x+=1
                y-=1
        elif junction_action == 2: # forward->left
            if self.at(2,1):
                y+=1
                x+=1

        self.x_pos = x
        self.y_pos = y
        self.transmit_position()

    def execute_action(self, action:int):
        if action == 0:
            pass
        elif action == 1:
            pass
        elif action == 2:
            pass
        elif action == 3:
            pass
        elif action == 4:
            pass
        elif action == 5:
            pass
        elif action == 6:
            pass
        elif action == 7:
            pass
        elif action == 8:
            pass
        elif action == 9:
            pass
        elif action == 10:
            pass
        elif action == 11:
            pass
        elif action == 12:
            pass
        elif action == 13:
            pass
        elif action == 14:
            pass
        elif action == 15:
            maqueenPlusV2.control_motor_stop(maqueenPlusV2.MyEnumMotor.ALL_MOTOR)
    
    # Radio functions
    
    def update_channel(self, radio_channel: int):
        radio.set_group(radio_channel)

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

    def transmit_action(self, action:int): # Encodes an action between 0x00 and 0xff to be sent between vehicles 
        send_num = action << 12
        send_num += (self.vehicle_id << 6)
        radio.send_number(send_num)


# Constants

# bitwise AND-ing this masks and the number that encodes info about the
# traffic situation then shifting the resulting number will
# yield different information from each part of the number

# First 4 bits are for scenario ID
# Next 2 bits are for vehicle ID
# Next 3 bits are for X position
# Next 3 bits are for Y position
ACTION_MASK = 0b1111000000000000
SCENARIO_MASK = 0b111100000000
ID_MASK = 0b11000000
POS_MASK = 0b111111
X_MASK = 0b111000
Y_MASK = 0b111

# Decode functions
def decode_action(encoded_num: int):
    return (ACTION_MASK & encoded_num) >> 12

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

# Initialize vehicle object

vehicle = Vehicle(..., ..., ..., ..., ..., ...)

# Return true if vehicle with id vehicle_id is at a valid coordinate
def is_at_valid_pos(vehicle_id: int):
    return vehicle.positions[vehicle_id] >= 0

def get_pos(vehicle_id: int):
    return (get_x(vehicle_id), get_y(vehicle_id))

def get_x(vehicle_id: int):
    return decode_x(vehicle.positions[vehicle_id])

def get_y(vehicle_id: int):
    return decode_y(vehicle.positions[vehicle_id])

# Radio functions 

def on_received_number(received_number: int):
    vehicle.interpret_information(received_number)

# Forever loop

def on_forever():
    pass

# Set-up 
radio.on_received_number(on_received_number)

# Initialize motors
maqueenPlusV2.i2c_init()

# IMPLEMENT PATH FINDING ALGORITHM

# IMPLEMENT CODE SPECIFIC TO EACH VEHICLE

basic.forever(on_forever)
