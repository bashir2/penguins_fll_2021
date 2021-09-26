# This is where we keep all the shared blocks. Please only include functions
# and constants in this file for now.

SHARPNESS = 0.7
SPEED = 300
WHEEL_CIRCUMFERENCE = 180

def follow_line(tank, left_cs, right_cs, millies):
    tank.reset()
    while tank.distance() < millies:
        subtract = left_cs.reflection() - right_cs.reflection() # subtracts color sensors
        multiply = subtract * SHARPNESS # multiplies the difference by 0.7
        tank.drive(SPEED, multiply) # follows the line 

def gyro_straight(tank, gyro, millies, target):
    tank.reset()
    while tank.distance() < millies:
        subtract = gyro.angle() - target  # subtracts color sensors
        multiply = subtract * SHARPNESS # multiplies the difference by 0.7
        tank.drive(SPEED, multiply) # follows the line

