#!/usr/bin/env pybricks-micropython
import blocks
import time
from robot import Robot
r = Robot()
#start at 83mm
r.arm_movement(millies=63, speed=-350, is_back=True, wait=False)
# Moves up at start
r.straight_distance(350)
r.tank.turn(10)
r.tank.turn(-70)
r.straight_distance(30)
r.straight_distance(-30)
r.tank.turn(70)
r.straight_distance(-30)
# Pushes the box
r.follow_line(290)
r.gyro_angle(145)
r.arm_movement(millies=146, speed=1500, is_back=True)
# Lowers plane door
#goes to zero height
r.arm_movement(millies=30, speed=-1500, is_back=True)
r.straight_distance(90)
r.gyro_angle(190)
#goes to zero height
r.arm_movement(millies=30, speed=300, is_back=True)
r.straight_distance(-75)
r.gyro_angle(135)
r.arm_movement(millies=60, speed=-300, is_back=True)
# Moves box in circle
r.gyro_angle(220)
r.straight_distance(-50)
r.arm_movement(millies=50, speed=1500, is_back=True)
r.straight_to_black(-150)
r.tank.turn(10)
r.straight_distance(30)
r.arm_movement(millies=200, speed=-1000, is_back=True)
r.straight_distance(1000, 1000)
