# This is where we keep all the shared blocks. Please only include functions
# and constants in this file for now.
import robot
import time

def go_to_bay(r, bay_num, init_distance, is_blue=False):
    '''
    Preconditions: 
        Arm at height: 120
    
    Postconditions:
        Arm at height: 85
    '''
    print('go_to_bay {}'.format(bay_num))
    if bay_num == 1:
        r.straight_distance(distance=11 - init_distance) # init value = 14
        r.gyro_angle(90)
    elif bay_num == 2:
        r.straight_distance(distance=120 - init_distance) # init value = 130
        r.gyro_angle(90)
    elif bay_num == 3:
        r.straight_distance(distance=180 - init_distance) # init value = 194
        r.gyro_angle(90)
    else:
        print('ERROR bay_num should be in [1,3] got {}'.format(bay_num))
    backward = -80
    forward = 88
    if is_blue:
        backward = 0
        forward = 80
    r.straight_distance(speed=80, distance=backward)
    r.arm_movement(speed=400, millies=80)
    r.straight_distance(forward) # init value = 86
    r.arm_movement(speed=-400, millies=45)
    r.straight_distance(distance=-10, speed=80)

def check_cargo(r):
    '''
    Preconditions: 
        Arm at height: 190 (3 holes)
    
    Postconditions:
        Arm at height: 120
    '''
    cargo1 = 0
    cargo2 = 0
    cargo3 = 0
    cargo1 = r.ultra.distance(silent=False)
    r.gyro_straight_distance(distance=100, target_angle=0)
    cargo2 = r.ultra.distance(silent=False)
    r.gyro_straight_distance(distance=100, target_angle=0)
    cargo3 = r.ultra.distance(silent=False)
    print('distance of the first cargo: ' + str(cargo1))
    print('distance of the second cargo: ' + str(cargo2))
    print('distance of the third cargo: ' + str(cargo3))
    # does train track
    r.straight_distance(speed=90, distance=17)
    r.arm_movement(speed=600, millies=127)  # arm at height: 63
    r.straight_distance(speed=90, distance=-26)
    r.arm_movement(speed=-600, millies=57, wait=False)  # arm at height: 120
    # At this point we are 144 mm from reference line

    if cargo1 < cargo2 and cargo1 < cargo3:
        green_loc = 1
        if cargo2 < cargo3:
            blue_loc = 3
        else:
            blue_loc = 2
    elif cargo2 < cargo1 and cargo2 < cargo3:
        green_loc = 2
        if cargo3 < cargo1:
            blue_loc = 1
        else:
            blue_loc = 3
    else:
        green_loc = 3
        if cargo1 < cargo2:
            blue_loc = 2
        else:
            blue_loc = 1
    go_to_bay(r, green_loc, init_distance=139)  # now arm at height 85
    cargo_connect(r, green_loc)
    return blue_loc


def cargo_connect(r, green_loc):
    '''
    Preconditions: 
        Arm at height: 85
    
    Postconditions:
        Arm at height: 120
    '''
    if green_loc == 1:
        r.gyro_angle(175)
        r.straight_to_black(speed=-80)
    elif green_loc == 2:
        r.gyro_angle(175)
        r.straight_to_black()
    else:
        r.steering_angle(speed=-100, sharpness=40, angle=38)
        r.steering_angle(speed=100, sharpness=86, angle=175)
        r.straight_to_black(speed=100)
        r.gyro_angle(177)
    r.straight_distance(80)
    r.arm_movement(speed=500, millies=56)
    r.straight_to_black(speed=-100)
    # move arm to height 120
    r.arm_movement(speed=-500, millies=91)


def blue_circle(r, bay_num):
    '''
    Preconditions: 
        Arm at height: 85
    
    Postconditions:
        Arm at height: 30
    '''
    angle = 269
    if bay_num == 1:
        r.steering_angle(speed=-150, sharpness=20, angle=120)
    elif bay_num == 2:
        r.straight_distance(-230)
    else: # this worked consistently
        r.steering_angle(speed=-150, sharpness=50, angle=0)
        angle = -75
    r.gyro_angle(angle=angle, speed=100)
    r.gyro_straight_distance(distance=150, target_angle=angle, speed=100)
    r.arm_movement(speed=600, millies=55)
    r.straight_distance(-200)


def pick_blue(r, blue_loc):
    '''
    Preconditions: 
        Arm at height: 120
    
    Postconditions:
        Arm at height: 30
    '''
    go_to_bay(r, blue_loc, init_distance=0, is_blue=True)
    # now arm is at height 85
    blue_circle(r, blue_loc)


def train(r):
    '''
    Preconditions: 
        Arm at height: 30
    
    Postconditions:
        Arm at height: 190
    '''
    r.arm_movement(speed=-1000, millies=160, wait=False)
    # now arm is at height 190  
    r.gyro_angle(-110)
    r.straight_to_black(speed=80)
    r.straight_distance(130) # init value = 165
    r.gyro_angle(-30)
    r.straight_distance(-60)
    r.follow_line(distance=200, speed=40, sharpness_color=0.7)
    r.gyro.reset_angle(-30)
    # fix the angle
    r.straight_to_black(speed=70)
    # At perpendicular line
    r.straight_distance(85)
    r.straight_distance(-85)
    # does helicopter
    r.straight_distance(-60)
    r.steering_angle(speed=-40, sharpness=40, angle=-160)
    r.straight_distance(-93)
    r.arm_movement(speed=400, millies=67, is_back=True)
    # Goes to train from fixed point and puts down the cargo boxes
    r.straight_distance(80)
