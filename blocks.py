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
        
        
def stop_on_black(left_cs, right_cs):
        if left_cs.reflection() <= 14:
            return True
        else:
            return False

        
def perpendicular_line(tank, left_cs, right_cs, line_distance, left_wheel, right_wheel):
    if line_distance >= 0:
        turn = 85
    else:
        turn = -85
    tank.settings(200, 100, 100, 100)
    tank.turn(turn)
    tank.straight(abs(line_distance))
    tank.turn(turn * -1)
    while not stop_on_black(left_cs, right_cs):
        tank.drive(100, 0)
    tank.stop()
