#!/usr/bin/env pybricks-micropython
''' The north path

This progrma does the north path in the following order:
1. Platooning truck
2. Briage
3. Airplane
4. Ship
5. Crane
6. Truck
'''

import robot
import time
import blocks


my_robot = robot.Robot()

# Write your program here.

# follow the line to push the truck and the bridge
my_robot.gyro_angle(-54)
my_robot.straight_distance(280)
my_robot.follow_line(520)
my_robot.arm_movement(-200, 52)
# truck and first bridge done 
my_robot.straight_distance(200)
my_robot.arm_movement(200, 32)
my_robot.straight_distance(-75)
# second bridge done

# maneuvers to hit the airplane
my_robot.arm_movement(-200, 20)
my_robot.steering(-2000, 18.5, 335) # initial value = 376
# airplane done

# preparing for the ship 
my_robot.steering_angle(speed=40, sharpness=16, angle=0)
print('angle after plane: ' + str(my_robot.gyro.angle()))
my_robot.gyro_angle(0)
my_robot.straight_distance(350)
my_robot.straight_to_black(speed=100, ignore_left=True)
# got to bridge black line
my_robot.arm_movement(speed=200, millies=25)
my_robot.straight_distance(distance=45, speed=100)
my_robot.gyro_angle(-88)
my_robot.straight_to_black(speed=100, ignore_right=True)
my_robot.brake()
my_robot.follow_line(115, speed=75)
# at ship
my_robot.straight_distance(3.6)
my_robot.arm_movement(speed=200, millies=13)
time.sleep(0.8)
my_robot.straight_distance(distance=-115, speed=17)
# ship done
my_robot.arm_movement(speed=-300, millies=125)
my_robot.straight_distance(60)
my_robot.gyro_angle(2)
my_robot.gyro_straight_distance(distance=140, target_angle=2, speed=50)
my_robot.gyro_angle(2)
my_robot.gyro_straight_distance(distance=90, target_angle=2, speed=50)
# crane done
my_robot.straight_distance(-40)
my_robot.gyro_angle(2)
my_robot.straight_distance(distance=-495, speed=2000)
# truck done

# maneuver for reference point
my_robot.straight_distance(200)
my_robot.gyro_angle(90)
my_robot.straight_to_black(speed=100)
my_robot.straight_distance(-20)
# at bridge black line
my_robot.steering_angle(speed=75, sharpness=50, angle=4)
my_robot.gyro_angle(4)
my_robot.gyro_straight_distance(distance=170, target_angle=4)
my_robot.straight_to_black(speed=100, ignore_left=True)
# at sorting center loose end
my_robot.straight_distance(130)
my_robot.gyro_angle(90)
my_robot.follow_line(distance=130, speed=70, sharpness_color=0.9)
my_robot.straight_to_black(ignore_right=True, speed=100)
my_robot.gyro.reset_angle(90)
# at sorting center
my_robot.straight_distance(-50)
my_robot.gyro_angle(2)
my_robot.straight_distance(-50)
my_robot.arm_movement(9)
