# Variables
base_speed = 75
distance = 0
error = 0
vehicle_detection_speed = 0

# Init
matrixLidarDistance.initialize(matrixLidarDistance.Addr.ADDR4,
    matrixLidarDistance.Matrix.MAT)
basic.pause(2500)
maqueenPlusV2.i2c_init()
radio.set_group(37)