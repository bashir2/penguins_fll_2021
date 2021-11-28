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
        self.tank = DriveBase(self.left_wheel, self.right_wheel, 52, 110)
        self.gyro = GyroSensor(Port.S1) 
        self.forklift = Motor(Port.D)
        self.back_forklift = Motor(Port.A)
        self.left_cs_thresh, self.right_cs_thresh = self.read_calibrate()
        print('Color sensor thresholds are left: {} right: {}'.format(
            self.left_cs_thresh, self.right_cs_thresh))
        self.ultra = UltrasonicSensor(Port.S4)

    def follow_line(self, distance, speed=100, sharpness_color=0.4):
        ''' Follows the line for a certain distance
    
        Args:
            distance: the amount of millilmeters the robot should travel
        '''
        self.tank.reset()
        while self.tank.distance() < distance:
            subtract = self.left_cs.reflection() - self.right_cs.reflection() 
            multiply = subtract * sharpness_color
            self.tank.drive(speed, multiply) 
        self.brake()


    def read_calibrate(self):
        file_handler = open("Calibration.txt", "r") # reads the value
        left_value = int(file_handler.readline())
        right_value = int(file_handler.readline())
        return left_value, right_value

    def brake(self):
        ''' brakes the robot
        '''
        # The next call sometimes fails on one motor.
        #self.tank.stop(Stop.BRAKE)
        # So trying the next approach instead.
        self.tank.stop(Stop.BRAKE)
        self.left_wheel.brake()
        self.right_wheel.brake()

    def gyro_straight(self, target, speed=SPEED):
        ''' Goes forward until it reaches black trying to keep gyro angle straight.
    
        Args:
            target: The amount of going forward in
        '''
        while not self.stop_on_black(): 
            subtract = self.gyro.angle() - target  
            multiply = subtract * (SHARPNESS * -1) 
            self.tank.drive(speed, multiply)
            #print(self.gyro.angle())
        self.brake() 
    
    
    def gyro_straight_distance(self, distance, target_angle, speed=100, sharpness=SHARPNESS):
        ''' Goes forward for a certain distance trying to keep gyro angle straight. 
    
        Args: 
            distance: how much millimeters the robot should travel
        '''
        self.tank.settings(200, 100, 30, 30)
        self.tank.reset()
        while abs(self.tank.distance()) < distance:
            subtract = self.gyro.angle() - target_angle 
            multiply = subtract * (sharpness * -1) 
            self.tank.drive(speed, multiply)
            # print(self.gyro.angle())
        self.brake()
    
    
    def arm_movement(self, speed=200, millies=0, is_back=False, wait=True):
        ''' Makes the robot arm go up/down for a certain amount of millimeters
    
        Args: 
            millies: the amount of millimeters the arm goes up/down  
            speed: the amount of speed the arm travels with 
        ''' 
        f = self.forklift
        degrees = millies * 10
        if is_back:
            f = self.back_forklift
            degrees *= -1  
        f.run_angle(speed, degrees, wait=wait)
        self.brake()
    
    
    def gyro_angle(self, angle, speed=150):
        ''' Turns to desired angle
        Args: 
        angle: the angle you want the robot to turn
        '''
        self.brake()
        big = angle + 2
        small = angle - 2
        self.tank.settings(speed, speed, speed, speed)
        print('Current angle= {} target= {}'.format(self.gyro.angle, angle))
        self.tank.turn(angle - self.gyro.angle())
        self.brake()
        # you need to brake here so that the motor can run
        while self.gyro.angle() <= small or self.gyro.angle() >= big:
            while self.gyro.angle() <= small or self.gyro.angle() >= big: 
                if self.gyro.angle() <= small:
                    self.left_wheel.run(TURN_SPEED)
                    self.right_wheel.run(TURN_SPEED * -1)
                else:
                    self.left_wheel.run(TURN_SPEED * -1)
                    self.right_wheel.run(TURN_SPEED)
            self.brake()
            time.sleep(0.4)    
        self.brake()
        print('gyro_angle end: ' + str(self.gyro.angle()))


    def stop_on_black(self, ignore_left=False, ignore_right=False):
        ''' Used so the robot can identify black
        '''
        if (self.left_cs.reflection() <= self.left_cs_thresh or ignore_left) and (
            self.right_cs.reflection() <= self.right_cs_thresh or ignore_right):
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
        while not self.stop_on_black(left_cs, right_cs):
            self.tank.drive(100, 0)
        self.brake()
    

    def steering(self, speed, sharpness, distance):
        ''' Makes the robot able to turn and go forward

        Args:
        speed: the speed the robot should travel with
        sharpness: how sharp the robot should turn
        distance: how far the robot should go
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
        time.sleep(0.3)
        print("End of steering_angle " + str(self.gyro.angle()))


    def straight_distance(self, distance, speed=200): 
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


    def straight_to_black(self, speed=150, ignore_left=False, ignore_right=False):
        ''' Goes straight until it reaches black
        '''
        while not self.stop_on_black(ignore_left, ignore_right):
            self.tank.drive(speed, 0)
        self.brake()
