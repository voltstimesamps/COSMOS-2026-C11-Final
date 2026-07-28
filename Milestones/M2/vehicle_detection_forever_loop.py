# Call to vehicle_detection function
def on_forever():
    global base_speed
    vehicle_detection_speed = vehicle_detection(200)
    base_speed = vehicle_detection_speed
basic.forever(on_forever)