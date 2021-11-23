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
        r.straight_distance(14 - init_distance) 
        r.gyro_angle(90)
    elif bay_num == 2:
        r.straight_distance(130 - init_distance)
        r.gyro_angle(90)
    elif bay_num == 3:
        r.straight_distance(169 - init_distance)
        r.gyro_angle(90) 
    else:
        print('ERROR bay_num should be in [1,3] got {}'.format(bay_num))
    d = 0
    forward = 0
    if is_blue:
        d = 80
        forward = 25
    r.straight_distance(speed=80, distance=-80 + d)
    r.arm_movement(speed=400, millies=80)
    r.straight_distance(92 - forward) # init value = 86
    r.arm_movement(speed=-400, millies=45)
    r.straight_distance(distance=-10, speed=100)
    return bay_num

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
    r.arm_movement(speed=400, millies=127)  # arm at height: 63
    r.straight_distance(speed=90, distance=-26)
    r.arm_movement(speed=-400, millies=57, wait=False)  # arm at height: 120
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
        r.steering_angle(speed=-100, sharpness=20, angle=48)
        r.steering_angle(speed=100, sharpness=66, angle=175)
        r.straight_to_black(speed=100)
        r.gyro_angle(175)
    r.straight_distance(100)
    r.arm_movement(speed=400, millies=56)
    r.straight_to_black(speed=-100)
    # move arm to height 120
    r.arm_movement(speed=-400, millies=91)


def blue_circle(r, bay_num):
    '''
    Preconditions: 
        Arm at height: 85
    
    Postconditions:
        Arm at height: 30
    '''
    if bay_num == 1:
        r.steering_angle(speed=-150, sharpness=20, angle=120)
    elif bay_num == 2:
        r.straight_distance(-230)
    else:
        r.steering_angle(speed=-150, sharpness=20, angle=60)
    r.gyro_angle(angle=260, speed=100)
    r.straight_distance(120)
    r.arm_movement(speed=200, millies=55)
    r.straight_distance(-200)


def pick_blue(r, blue_loc):
    '''
    Preconditions: 
        Arm at height: 120
    
    Postconditions:
        Arm at height: 30
    '''
    bay_num = go_to_bay(r, blue_loc, init_distance=0, is_blue=True)
    # now arm is at height 85
    blue_circle(r, bay_num)


def train(r):
    '''
    Preconditions: 
        Arm at height: 30
    
    Postconditions:
        Arm at height: 190
    '''
    print('train started')
    r.arm_movement(speed=-500, millies=160, wait=False)
    # now arm is at height 190  
    r.gyro_angle(240)
    r.straight_to_black(speed=80)
    r.straight_distance(140) # init value = 165
    r.gyro_angle(330)
    r.straight_distance(-100)
    r.follow_line(distance=150, speed=40)
    r.gyro.reset_angle(-30)
    # fix the angle
    r.straight_to_black(speed=70)
    # At perpendicular line
    r.straight_distance(85)
    r.straight_distance(-85)
    # does helicopter
    r.straight_distance(-60)
    r.steering_angle(speed=-40, sharpness=50, angle=-170)
    time.sleep(0.5)
    r.straight_distance(-86)
    r.arm_movement(speed=400, millies=63, is_back=True)
    # Goes to train from fixed point and puts down the cargo boxes
    r.straight_distance(80)
