#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

#import blocks

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.

# Create your objects here. 
ev3 = EV3Brick()
left_wheel = Motor(Port.B)
right_wheel = Motor(Port.C)
left_cs = ColorSensor(Port.S2)
right_cs = ColorSensor(Port.S3)
tank = DriveBase(left_wheel, right_wheel, 50, 110)
gyro = GyroSensor(Port.S1, Direction.CLOCKWISE) 

# Write your program here.

import blocks 

blocks.gyro_straight(tank, gyro, 600, 0)

blocks.follow_line(tank, left_cs, right_cs, 100)

#import run_selected

#tank.straight(blocks.WHEEL_CIRCUMFERENCE * 4)
tank.stop()

ev3.speaker.say('ok') # says 'ok' to check
#blocks.follow_line(tank, left_cs, right_cs, blocks.WHEEL_CIRCUMFERENCE * 3)
tank.stop()

ev3.speaker.say('ha ha ha') # says 'ha ha ha' when done
