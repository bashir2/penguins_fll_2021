# This is where we keep all the shared blocks. Please only include functions
# and constants in this file for now.
import time


SHARPNESS = 3
SHARPNESS_COLOR = 0.7 
SPEED = 100
WHEEL_CIRCUMFERENCE = 180
TURN_SPEED = 45


def follow_line(tank, left_cs, right_cs, millies):
    ''' Follows the line for a certain distance

    Args:
        millies: the amount of millilmeters the robot should travel
    '''
    tank.reset()
    while tank.distance() < millies:
        subtract = left_cs.reflection() - right_cs.reflection() 
        multiply = subtract * SHARPNESS_COLOR
        tank.drive(SPEED, multiply) 
    tank.stop()


def gyro_straight(tank, gyro, left_cs, right_cs, target):
    ''' Goes forward until it reaches black trying to keep gyro angle straight.

    Args:
        target: The amount of going forward in
    '''
    tank.settings(200, 100, 30, 30)
    while not stop_on_black(left_cs, right_cs): 
        subtract = gyro.angle() - target  
        multiply = subtract * (SHARPNESS * -1) 
        tank.drive(SPEED, multiply)
        print(gyro.angle())
    tank.stop() 


def gyro_straight_distance(tank, gyro, millies, target):
    ''' Goes forward for a certain distance trying to keep gyro angle straight. 

    Args: 
        millies: how much millimeters the robot should travel
    '''
    tank.settings(200, 100, 30, 30)
    tank.reset()
    while tank.distance() < millies:
        subtract = gyro.angle() - target 
        multiply = subtract * (SHARPNESS * -1) 
        tank.drive(SPEED, multiply)
        print(gyro.angle())
    tank.stop()


def arm_movement(forklift, speed, millies):
    ''' Makes the robot arm go up/down for a certain amount of millimeters

    Args: 
        millies: the amount of millimeters the arm goes up/down  
        speed: the amount of speed the arm travels with 
    ''' 
    degrees = millies * 10  
    forklift.run_angle(speed, degrees)


def gyro_angle( tank, gyro, left_wheel, right_wheel, angle):
    gyro.reset_angle(0)
    big = angle + 1
    small = angle - 1
    while gyro.angle() <= small or gyro.angle() >= big:
        while gyro.angle() <= small or gyro.angle() >= big: 
            if gyro.angle() <= small:
                left_wheel.run(TURN_SPEED)
                right_wheel.run(TURN_SPEED * -1)
            else:
                left_wheel.run(TURN_SPEED * -1)
                right_wheel.run(TURN_SPEED)
        tank.stop()
        time.sleep(0.5)
        print(gyro.angle())

def stop_on_black(left_cs, right_cs):
    ''' Used so the robot can identify black
    '''
    if left_cs.reflection() <= 9 and right_cs.reflection() <= 9:
        return True
    else:
        return False


def perpendicular_line(tank, left_cs, right_cs, line_distance, left_wheel, right_wheel):
    ''' The robot goes to an intersection of lines to create a reference point

    Args:
        line_distance: the distance of your end-point 
            on the line from the intersection of the two lines
    '''
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


def go_to_coordinate(tank, gyro_sensor, left_wheel, right_wheel, targetx, targety):
    # The assumption is that the robot is at (0,0) along x axis. 
    slope = targety/targetx
    angle = math.atan(slope)
    angle_degrees = math.degrees(angle)
    gyro_angle(tank, gyro_sensor, left_wheel, right_wheel, angle_degrees * -1)
    length = math.sqrt(targetx**2 + targety**2)
    tank.straight(length)
    tank.stop()


def steering(tank, speed, sharpness, millies):
    tank.reset()
    big = millies
    small = -1 * millies
    while tank.distance() >= small and tank.distance() <= big:
        tank.drive(speed, sharpness)
    tank.stop()   

    
def steering_angle(tank, gyro, speed, sharpness, angle):
    big = angle + 1
    small = angle - 1
    while gyro.angle() <= small or gyro.angle() >= big:
        tank.drive(speed, sharpness)
    tank.stop()
