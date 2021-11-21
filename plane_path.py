#!/usr/bin/env pybricks-micropython
import blocks
import time
from robot import Robot
r = Robot()
r.arm_movement(millies=55, speed=-350, is_back=True)
# Moves arm up at start
r.tank.straight(360)

r.tank.turn(-60)

r.tank.straight(50)

r.tank.straight(-50)

r.tank.turn(60)

r.tank.straight(-60)

# Push's the box

r.follow_line(250)

r.tank.straight(80)

r.tank.turn(95)

r.tank.straight(-5)

r.arm_movement(millies=110, speed=1500, is_back=True)

# Push down handle thinky ma bobber

r.arm_movement(millies=30, speed=-1500, is_back=True)

r.tank.straight(90)

r.tank.turn(55)

r.arm_movement(millies=80, speed=300, is_back=True)

r.tank.straight(-60)

r.tank.turn(-50)

# Moves box in circle

r.tank.turn(100)

time.sleep(3)

r.tank.turn(-30)

time.sleep(3)

r.tank.straight(-50)

time.sleep(3)

r.tank.turn(30)

time.sleep(3)

r.arm_movement(millies=15, speed=-1500, is_back=True)

time.sleep(3)

r.straight_to_black(-150)

r.tank.turn(10)

time.sleep(3)

r.tank.straight(30)

time.sleep(3)

r.arm_movement(millies=100, speed=-1000, is_back=True)

time.sleep(3)

r.tank.straight(80)

r.tank.turn(-35)

r.tank.straight(50)

r.tank.turn(35)

r.tank.straight(80)
