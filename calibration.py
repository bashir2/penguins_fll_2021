#!/usr/bin/env python3   
import time 
from robot import 
import main
from pybricks.parameters import Button
def calibration(ev3, left_cs, right_cs, right_wheel, left_wheel): #add any extra sensor/motors, I can not as I would get an error
    button_pressed = False
    counter = 0
    delay = 75
    while button_pressed == False:
        left_cs_string = "Left CS:", str(left_cs.reflection())
        right_cs_string = "Right CS:", str(right_cs.reflection())
        left_wheel_string = "Left Wheel:", str(left_wheel.angle())
        right_wheel_string = "Right Wheel:", str(right_wheel.angle())
        ev3.screen.draw_text(0, 0, left_cs_string)
        ev3.screen.draw_text(0, 30, right_cs_string)
        ev3.screen.draw_text(0, 60, left_wheel_string)
        ev3.screen.draw_text(0, 90, right_wheel_string)
        print(ev3.buttons.pressed())
        time.sleep(0.2)
        ev3.screen.clear()
        if(ev3.buttons.pressed() == [Button.CENTER]):
            button_pressed = True
        else:
            button_pressed = False
    str_value = str(left_cs.reflection())
    file_handler = open("Calibration.txt", "w")
    file_handler.write(str_value)
    file_handler.close()
        

calibration(Robot.ev3, Robot.left_cs, Robot.right_cs, Robot.right_wheel, Robot.left_wheel)
