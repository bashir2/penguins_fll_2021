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
r.follow_line(510)
r.arm_movement(-400, 52)
# truck and first bridge done 
r.straight_distance(190) # init value = 200
r.arm_movement(400, 32)
r.straight_distance(-75)
# second bridge done

# maneuvers to hit the airplane
r.arm_movement(-400, 20)
r.steering(-2000, 18.5, 310)
# airplane done

# preparing for the ship 
r.gyro_angle(0)
print('angle after plane: ' + str(r.gyro.angle()))
r.gyro_angle(0)
r.straight_distance(380)
r.straight_to_black(speed=100, ignore_right=True)
# got to bridge black line
r.arm_movement(speed=400, millies=25, wait=False)
r.straight_distance(distance=45, speed=100)
r.gyro_angle(-90)
r.straight_to_black(speed=100, ignore_right=True)
r.follow_line(115, speed=75)
# at ship
r.straight_distance(3.26)
r.arm_movement(speed=200, millies=13)
time.sleep(0.8)
r.straight_distance(distance=-125, speed=17)
# ship done
r.arm_movement(speed=-400, millies=125)
r.straight_distance(60)
r.gyro_angle(0)
r.gyro_straight_distance(distance=140, target_angle=0, speed=50)
r.gyro_angle(0)
r.gyro_straight_distance(distance=90, target_angle=0, speed=50)
# crane done
r.straight_distance(-40)
r.gyro_angle(3) 
r.gyro_straight_distance(distance=455, speed=-2000, target_angle=3, sharpness=1)
# truck done

# maneuver for reference point
r.straight_distance(200)
r.gyro_angle(90)
r.straight_to_black(speed=100)
r.straight_distance(-25)
# at bridge black line
r.steering_angle(speed=75, sharpness=50, angle=3)
r.gyro_angle(3)
r.gyro_straight_distance(distance=170, target_angle=2)
r.straight_to_black(speed=100, ignore_left=True)


# at sorting center loose end
r.straight_distance(125)
r.gyro_angle(90)
r.follow_line(distance=130, speed=40, sharpness_color=0.7)
r.gyro.reset_angle(90)
r.straight_to_black(ignore_right=True, speed=100)
# at sorting center
r.straight_distance(speed=80, distance=-50)
r.gyro_angle(0)
r.straight_distance(speed=80, distance=-50)
# picking up green crate
blue_loc = blocks.check_cargo(r)
# does CARGO CONNECT circle

r.straight_distance(60)
r.gyro_angle(90)
r.follow_line(distance=40, speed=40, sharpness_color=0.4)
r.straight_to_black(ignore_right=True, speed=100)
# at sorting center again
r.straight_distance(-50)
r.gyro_angle(0)
# picks up the blue
blocks.pick_blue(r, blue_loc)
# does the train
blocks.train(r)
