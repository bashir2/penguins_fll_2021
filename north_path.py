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
my_robot.steering(-1000, 19.3, 394)
# airplane done

# preparing for the ship 
my_robot.steering_angle(speed=40, sharpness=-6, angle=2)
print('angle after plane: ' + str(my_robot.gyro.angle()))
my_robot.gyro_angle(2)
my_robot.straight_distance(380)
my_robot.straight_to_black(speed=100, ignore_left=True)
# got to black line
my_robot.arm_movement(speed=200, millies=25)
my_robot.straight_distance(30)
my_robot.gyro_angle(-89)
my_robot.straight_to_black(speed=100, ignore_right=True)
my_robot.brake()
my_robot.follow_line(105, speed=75)
# at ship
my_robot.straight_distance(2.25)
my_robot.arm_movement(speed=200, millies=17)
time.sleep(0.3)
my_robot.straight_distance(distance=-130, speed=50)
# ship done
my_robot.arm_movement(speed=-300, millies=125)
my_robot.straight_distance(60)
my_robot.gyro_angle(10)
my_robot.gyro_straight_distance(millies=260, target_angle=10, speed=100)
# crane done
my_robot.straight_distance(-20)
my_robot.gyro_angle(12.3)
my_robot.straight_distance(distance=-550, speed=1000)
# truck done
