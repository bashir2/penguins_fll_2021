#!/usr/bin/env pybricks-micropython
''' The north path

This program does the north path in the following order:
1. Platooning truck
2. Bridge
3. Airplane
4. Ship
5. Crane
6. Truck
'''

import robot
import time
import blocks


r = robot.Robot()

# Write your program here.

# follow the line to push the truck and the bridge
r.gyro_angle(-54) 
r.straight_distance(280)
r.follow_line(520, sharpness_color=0.5)
r.arm_movement(-200, 52)
# truck and first bridge done 
r.straight_distance(180) # init value = 200
r.arm_movement(200, 32)
r.straight_distance(-75)
# second bridge done

# maneuvers to hit the airplane
r.arm_movement(-200, 20)
r.steering(-2000, 18.5, 315) 
# airplane done

# preparing for the ship 
r.steering_angle(speed=40, sharpness=16, angle=0)
print('angle after plane: ' + str(r.gyro.angle()))
r.gyro_angle(0)
r.straight_distance(350)
r.straight_to_black(speed=100, ignore_left=True)
# got to bridge black line
r.arm_movement(speed=200, millies=25)
r.straight_distance(distance=45, speed=100)
r.gyro_angle(-88)
r.straight_to_black(speed=100, ignore_right=True)
r.brake()
r.follow_line(115, speed=75)
# at ship
r.straight_distance(6.6)
r.arm_movement(speed=200, millies=13)
time.sleep(0.8)
r.straight_distance(distance=-115, speed=17)
# ship done
r.arm_movement(speed=-300, millies=125)
r.straight_distance(60)
r.gyro_angle(2)
r.gyro_straight_distance(distance=140, target_angle=2, speed=50)
r.gyro_angle(2)
r.gyro_straight_distance(distance=90, target_angle=2, speed=50)
# crane done
r.straight_distance(-40)
r.gyro_angle(3) 
r.straight_distance(distance=-495, speed=2000)
# truck done

# maneuver for reference point
r.straight_distance(200)
r.gyro_angle(90)
r.straight_to_black(speed=100)
r.straight_distance(-35)
# at bridge black line
r.steering_angle(speed=75, sharpness=50, angle=6)
r.gyro_angle(6)
r.gyro_straight_distance(distance=170, target_angle=6)
r.straight_to_black(speed=100, ignore_left=True)


# at sorting center loose end
r.straight_distance(155)
r.gyro_angle(87)
r.follow_line(distance=130, speed=40, sharpness_color=1.5)
r.gyro.reset_angle(90)
r.straight_to_black(ignore_right=True, speed=100)
# at sorting center
r.straight_distance(speed=80, distance=-50)
r.gyro_angle(2)
r.straight_distance(speed=80, distance=-50)
# picking up green crate
blue_loc = blocks.check_cargo(r)
# does CARGO CONNECT circle

r.straight_distance(60)
r.gyro_angle(90)
r.follow_line(distance=40, speed=40, sharpness_color=1.5)
r.straight_to_black(ignore_right=True, speed=100)
# at sorting center again
r.straight_distance(-50)
r.gyro_angle(2)
# picks up the blue
blocks.pick_blue(r, blue_loc)
# does the train
blocks.train(r)

# goes for the accident avoidance
r.gyro_straight_distance(speed=500, distance=450, target_angle=-90)
r.straight_to_black()
r.gyro_angle(-90)
r.ev3.speaker.say('hi')
r.gyro_angle(270)
r.straight_to_black()
r.steering(speed=400, sharpness=-55, distance=320)
r.straight_to_black()
r.straight_distance(66)
