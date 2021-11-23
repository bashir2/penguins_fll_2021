#!/usr/bin/env pybricks-micropython
import time 
from robot import Robot

from pybricks.parameters import Button
from pybricks.media.ev3dev import Font

if __name__ == "__main__":
    r = Robot()

    button_pressed = False
    r.ev3.screen.set_font(Font(family=None, size=12, bold=True))
    while button_pressed == False:
        left_cs_string = "Left CS:", str(r.left_cs.reflection())
        right_cs_string = "Right CS:", str(r.right_cs.reflection())
        left_wheel_string = "Left Wheel:", str(r.left_wheel.angle())
        right_wheel_string = "Right Wheel:", str(r.right_wheel.angle())
        ultra_string = "US:", str(r.ultra.distance(False))
        gyro_string = "Gyro:", str(r.gyro.angle())
        curr_value_string = "CV(LR): {} {}".format(r.left_cs_thresh, r.right_cs_thresh)
        r.ev3.screen.draw_text(0, 0, left_cs_string)
        r.ev3.screen.draw_text(0, 20, right_cs_string)
        r.ev3.screen.draw_text(0, 40, curr_value_string)
        r.ev3.screen.draw_text(0, 60, left_wheel_string)
        r.ev3.screen.draw_text(0, 80, right_wheel_string)
        r.ev3.screen.draw_text(105, 0, ultra_string)
        r.ev3.screen.draw_text(100, 20, gyro_string)

        time.sleep(0.2)
        r.ev3.screen.clear()
        if(r.ev3.buttons.pressed() == [Button.CENTER]):
            button_pressed = True
        else:
            button_pressed = False
    left_val = r.left_cs.reflection() + 1
    right_val = r.right_cs.reflection() + 1
    str_value = '{}\n{}'.format(left_val, right_val) 
    file_handler = open("Calibration.txt", "w")
    file_handler.write(str_value)
    file_handler.close()
