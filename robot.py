import time
import math

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

SHARPNESS = 3
SHARPNESS_COLOR = 0.7 
SPEED = 100
WHEEL_CIRCUMFERENCE = 180
TURN_SPEED = 30

class Robot():
    def __init__(self):
        self.ev3 = EV3Brick()
        self.left_wheel = Motor(Port.B)
        self.right_wheel = Motor(Port.C)
        self.left_cs = ColorSensor(Port.S2)
        self.right_cs = ColorSensor(Port.S3)
        self.ultra = UltrasonicSensor(Port.S4)
        self.tank = DriveBase(self.left_wheel, self.right_wheel, 50, 110)
        self.gyro = GyroSensor(Port.S1)
        self.lift = Motor(Port.A)
        self.cs_threshold = self.read_calibrate()


    def follow_line(self, millies, speed=100):
        ''' Follows the line for a certain distance
    
        Args:
            millies: the amount of millilmeters the robot should travel
        '''
        self.tank.reset()
        while self.tank.distance() < millies:
            subtract = self.left_cs.reflection() - self.right_cs.reflection() 
            multiply = subtract * SHARPNESS_COLOR
            self.tank.drive(speed, multiply) 
        self.brake()

    def follow_line_to_black(self, speed=100):
        '''  Follows the line untill both sensors are on black
        '''
        while not self.stop_on_black(): 
            subtract = self.left_cs.reflection() - self.right_cs.reflection() 
            multiply = subtract * SHARPNESS_COLOR
            self.tank.drive(speed, multiply) 
        self.brake()

    def read_calibrate(self):
        file_handler = open("Calibration.txt", "r")
        int_value = int(file_handler.read())
        return int_value

    def brake(self):
        ''' brakes the robot
        '''
        # The next call sometimes fails on one motor.
        #self.tank.stop(Stop.BRAKE)
        # So trying the next approach instead.
        self.tank.stop()
        self.right_wheel.brake()
        self.left_wheel.brake()

    def gyro_straight(self, target, speed=SPEED):
        ''' Goes forward until it reaches black trying to keep gyro angle straight.
    
        Args:
            target: The amount of going forward in
        '''
        while not self.stop_on_black(): 
            subtract = self.gyro.angle() - target  
            multiply = subtract * (SHARPNESS * -1) 
            self.tank.drive(speed, multiply)
        self.brake() 
    
    
    def gyro_straight_distance(self, millies, target_angle, speed=100):
        ''' Goes forward for a certain distance trying to keep gyro angle straight. 
    
        Args: 
            millies: how much millimeters the robot should travel
        '''
        self.tank.settings(200, 100, 30, 30)
        self.tank.reset()
        while self.tank.distance() < millies:
            subtract = self.gyro.angle() - target_angle 
            multiply = subtract * (SHARPNESS * -1) 
            self.tank.drive(speed, multiply)
        self.brake()
    
    
    def arm_movement(self, speed=200, millies=0):
        ''' Makes the robot arm go up/down for a certain amount of millimeters
    
        Args: 
            millies: the amount of millimeters the arm goes up/down  
            speed: the amount of speed the arm travels with 
        ''' 
        degrees = millies * 10  
        self.forklift.run_angle(speed, degrees)
        self.brake()
    
    def gyro_angle(self, angle):
        self.brake()
        big = angle + 1
        small = angle - 1
        print('gyro_angle begin: ' + str(self.gyro.angle()))
        while self.gyro.angle() <= small or self.gyro.angle() >= big:
            while self.gyro.angle() <= small or self.gyro.angle() >= big:
                speed = TURN_SPEED
                if abs(self.gyro.angle() - angle) > 5:
                    speed = 100 
                if self.gyro.angle() <= small:
                    self.left_wheel.run(speed)
                    self.right_wheel.run(speed * -1)
                else:
                    self.left_wheel.run(speed * -1)
                    self.right_wheel.run(speed)
            self.brake()
            time.sleep(0.4)    
        self.brake()
        print('gyro_angle end: ' + str(self.gyro.angle()))


    def stop_on_black(self, ignore_left=False, ignore_right=False):
        ''' Used so the robot can identify black
        '''
        if (self.left_cs.reflection() <= self.cs_threshold or ignore_left) and (
            self.right_cs.reflection() <= self.cs_threshold or ignore_right):
            self.brake()
            return True
        else:
            return False
    
    
    def perpendicular_line(self, line_distance):
        ''' The robot goes to an intersection of lines to create a reference point
    
        Args:
            line_distance: the distance of your end-point 
                on the line from the intersection of the two lines
        '''
        if line_distance >= 0:
            turn = 85
        else:
            turn = -85
        self.tank.settings(200, 100, 100, 100)
        self.tank.turn(turn)
        self.tank.straight(abs(line_distance))
        self.tank.turn(turn * -1)
        while not stop_on_black(left_cs, right_cs):
            self.tank.drive(100, 0)
        self.brake()
    

    def steering(self, speed, sharpness, distance):
        ''' Makes the robot able to turn and go forward
        Args:
        '''
        self.tank.reset()
        big = distance
        small = -1 * distance
        while self.tank.distance() >= small and self.tank.distance() <= big:
            self.tank.drive(speed, sharpness)
        self.brake()   
    
    def steering_angle(self, speed, sharpness, angle):
        ''' Steers the robot forward with `speed` and `sharpness` until a certain angle

        Preconditions:
            sharpness: should always be positive 

        Args:
            speed: the speed of the steering
            sharpness: the sharpness or urgency
            angle: the angle the robot is aiming to stop at
        '''
        print("Beginning of steering_angle " + str(self.gyro.angle()))
        big = angle + 1
        small = angle - 1
        temp_sharp = sharpness
        if self.gyro.angle() > angle:  # Should turn left
            temp_sharp = sharpness * -1
            while self.gyro.angle() <= small or self.gyro.angle() >= big:
                if self.gyro.angle() >= big:
                    self.tank.drive(speed, temp_sharp)
                elif self.gyro.angle() <= small:
                    self.tank.drive(speed * -1, temp_sharp * -1)
        elif self.gyro.angle() < angle:  # Should turn right
            while self.gyro.angle() <= small or self.gyro.angle() >= big:
                if self.gyro.angle() <= small:
                    self.tank.drive(speed, temp_sharp)
                elif self.gyro.angle() >= big:
                    self.tank.drive(speed * -1, temp_sharp * -1)
        self.brake()
        print("End of steering_angle " + str(self.gyro.angle()))

    def straight_distance(self, distance, speed=150):
        ''' Goes straight for a certain distance
        Args:
            speed: the speed of the robot
            distance: the distance the robot should go
                straight
        '''
        self.tank.reset()
        if distance < 0:
            speed = speed * -1 
        while abs(self.tank.distance()) < abs(distance):
            self.tank.drive(speed, 0)
        self.brake()


    def straight_to_black(self, speed, ignore_left=False, ignore_right=False):
        ''' Goes straight until it reaches black
        '''
        while not self.stop_on_black(ignore_left, ignore_right):
            self.tank.drive(speed, 0)
        self.brake()
                
    
