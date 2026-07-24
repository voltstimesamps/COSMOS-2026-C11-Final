# Goals: 
# - Store vehicle name (optional)
# - Store vehicle id
# - Store position
# - Initalize Radio
# - Transmit position

class Vehicle:
    def __init__(self,  vehicle_id: int, name:str, radio_channel: int=37):
        radio.set_group(radio_channel)
        # police =      0b00 = 0
        # ambulance =   0b01 = 1
        # drunk =       0b10 = 2
        # good =        0b11 = 3
        self.name = name
        self.vehicle_id = vehicle_id

        #   0 1 2 3 4
        # 0 @ @ @ @ @
        # 1 @   @   @
        # 2 @ @ @ @ @
        # 3 @   @   @
        # 4 @ @ @ @ @

        self.x_pos = 0 # Value between 0 and 4 (0b100) based on map above
        self.y_pos = 0 # Value between 0 and 4 (0b100) based on map above

    def update_channel(self, radio_channel: int):
        radio.set_group(radio_channel)

    def set_x(self, x_new): # Set internal x_pos to new x_pos
        self.x_pos = x_new
        self.transmit_position()
                
    def shift_x(self, dx):
        self.x_pos += dx # Shift inter x_pos by dx
        self.transmit_position()
        
    def set_y(self, y_new): # Set internal y_pos to new y_pos
        self.y_pos = y_new    
        self.transmit_position()
        
    def shift_y(self, dy):
        self.y_pos += dy # Shift inter x_pos by dx
        self.transmit_position()
        
    def transmit_position(self):
        # bits 0, 1 for vehicle id (4 possible IDs)
        # bits 2, 3, 4 for x position (5 possible positions)
        # bits 5, 6, 7 for y position (5 possible positions)
        send_num = self.vehicle_id
        send_num <<= 3
        send_num += self.x_pos
        send_num <<= 3
        send_num += self.y_pos
        radio.send_number(send_num)

def on_button_pressed_a(vehicle):
    vehicle.set_x((vehicle.x_pos+1) % 5)

def on_button_pressed_b(vehicle):
    vehicle.set_y((vehicle.y_pos+1) % 5)

vehicle = Vehicle(..., ..., ...):

while True:
    input.on_button_pressed(Button.A, on_button_pressed_a)
    input.on_button_pressed(Button.B, on_button_pressed_b)
    ...
