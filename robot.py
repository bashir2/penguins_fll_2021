import time

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
TURN_SPEED = 45

class Robot():
    def __init__(self):
        self.ev3 = EV3Brick()
        self.left_wheel = Motor(Port.B)
        self.right_wheel = Motor(Port.C)
        self.left_cs = ColorSensor(Port.S2)
        self.right_cs = ColorSensor(Port.S3)
        self.tank = DriveBase(self.left_wheel, self.right_wheel, 50, 110)
        self.gyro = GyroSensor(Port.S1) 
        self.forklift = Motor(Port.D)

    def follow_line(self, millies):
        ''' Follows the line for a certain distance
    
        Args:
            millies: the amount of millilmeters the robot should travel
        '''
        self.tank.reset()
        while self.tank.distance() < millies:
            subtract = self.left_cs.reflection() - self.right_cs.reflection() 
            multiply = subtract * SHARPNESS_COLOR
            self.tank.drive(SPEED, multiply) 
        self.tank.stop()
    

    def gyro_straight(self, target):
        ''' Goes forward until it reaches black trying to keep gyro angle straight.
    
        Args:
            target: The amount of going forward in
        '''
        self.tank.settings(200, 100, 30, 30)
        while not self.stop_on_black(): 
            subtract = self.gyro.angle() - target  
            multiply = subtract * (SHARPNESS * -1) 
            self.tank.drive(SPEED, multiply)
            print(self.gyro.angle())
        self.tank.stop() 
    
    
    def gyro_straight_distance(self, millies, target):
        ''' Goes forward for a certain distance trying to keep gyro angle straight. 
    
        Args: 
            millies: how much millimeters the robot should travel
        '''
        self.tank.settings(200, 100, 30, 30)
        self.tank.reset()
        while self.tank.distance() < millies:
            subtract = self.gyro.angle() - target 
            multiply = subtract * (SHARPNESS * -1) 
            self.tank.drive(SPEED, multiply)
            print(self.gyro.angle())
        self.tank.stop()
    
    
    def arm_movement(self, speed, millies):
        ''' Makes the robot arm go up/down for a certain amount of millimeters
    
        Args: 
            millies: the amount of millimeters the arm goes up/down  
            speed: the amount of speed the arm travels with 
        ''' 
        degrees = millies * 10  
        self.forklift.run_angle(speed, degrees)
    
    
    def gyro_angle(self, angle):
        self.gyro.reset_angle(0)
        big = angle + 1
        small = angle - 1
        while self.gyro.angle() <= small or self.gyro.angle() >= big:
            while self.gyro.angle() <= small or self.gyro.angle() >= big: 
                if self.gyro.angle() <= small:
                    self.left_wheel.run(TURN_SPEED)
                    self.right_wheel.run(TURN_SPEED * -1)
                else:
                    self.left_wheel.run(TURN_SPEED * -1)
                    self.right_wheel.run(TURN_SPEED)
            self.tank.stop()
            time.sleep(0.5)
            print(self.gyro.angle())
    
    def stop_on_black(self):
        ''' Used so the robot can identify black
        '''
        if self.left_cs.reflection() <= 9 and self.right_cs.reflection() <= 9:
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
        self.tank.stop()
    
    def steering(self, speed, sharpness, millies):
        self.tank.reset()
        big = millies
        small = -1 * millies
        while self.tank.distance() >= small and self.tank.distance() <= big:
            self.tank.drive(speed, sharpness)
        self.tank.stop()   
    
    def steering_angle(self, speed, sharpness, angle):
        big = angle + 1
        small = angle - 1
        while self.gyro.angle() <= small or self.gyro.angle() >= big:
            self.tank.drive(speed, sharpness)
        self.tank.stop()
    
