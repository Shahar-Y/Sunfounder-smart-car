#!/usr/bin/env python
import RPi.GPIO as GPIO
import video_dir
import car_dir
import motor
from time import ctime          # Import necessary modules
from pynput import keyboard
import time
import random

lastChar = -1
spd = 50
print 'hello!'
busnum = 1
# ctrl_cmd = ['forward', 'backward', 'left', 'right', 'stop', 'read cpu_temp', 'home', 'distance', 'x+', 'x-', 'y+', 'y-', 'xy_home']
video_dir.setup(busnum=busnum)
car_dir.setup(busnum=busnum)
motor.setup(busnum=busnum)     # Initialize the Raspberry Pi GPIO connected to the DC motor. 
video_dir.home_x_y()
car_dir.home()


   
motor.setSpeed(spd)
enableApple = False
enableFollowMode = False

def locate_and_center(x_pos, y_pos, obj_width, obj_height, screen_height, screen_width):
    global enableApple
    if enableApple:
        screen_center_x = screen_width/2
        screen_center_y = screen_height/2
        center_threshhold_x = screen_width/7
        center_threshhold_y = screen_height/7
        obj_center_x = x_pos + obj_width/2 
        obj_center_y = y_pos + obj_height/2
        
        if ( obj_center_x > screen_center_x + center_threshhold_x ):
            video_dir.move_increase_x()
        elif ( obj_center_x < screen_center_x - center_threshhold_x ):
            video_dir.move_decrease_x()
        
        if ( obj_center_y > screen_center_y + center_threshhold_y ):
            video_dir.move_increase_y()
        elif ( obj_center_y < screen_center_y - center_threshhold_y ):
            video_dir.move_decrease_y()

in_gesture = False
def locate_and_follow(x_pos, y_pos, obj_width, obj_height, screen_height, screen_width):
    global enableFollowMode
    global in_gesture
    # print video_dir.get_x()
    if (not in_gesture):
        if enableFollowMode:
            screen_center_x = screen_width/2
            screen_center_y = screen_height/2
            center_threshhold_x = screen_width/7
            center_threshhold_y = screen_height/7
            obj_center_x = x_pos + obj_width/2 
            obj_center_y = y_pos + obj_height/2

            x = video_dir.get_x()
            print x
            if (x > 321 and x < 381):
                    car_dir.home()
            else:
                if x < 351:
                    car_dir.turn_right()
                else:
                    car_dir.turn_left()
            if (obj_width * obj_height <= screen_height * screen_width * 0.25):
                motor.forward()
                print "too far!"
            elif (obj_width * obj_height > screen_height * screen_width * 0.5):
                motor.backward()
                print "too close!"
            else:
                motor.stop()
                print "perfect!"
                time_modulu = time.time() % 5
                print time_modulu
                
                if( int(time_modulu) == 0):
                    print "time modulu is 0!"
                    rnd = random.randint(0,6)
                    print "RANDOM IS: "
                    print rnd
                    in_gesture = True
                    if (rnd == 0):
                            nod_yes(3)
                    elif (rnd == 1):
                            nod_no(3)
                    elif (rnd == 2):
                            circle_head(2)
                    elif (rnd == 3):
                            look_right()
                    elif (rnd == 4):
                            look_left()
                    elif (rnd == 5):
                            look_up()
                    elif (rnd == 6):
                            look_down()
                    print "DONE WITH RANDOM. in_gesture: " + in_gesture + rnd
                    in_gesture = False

            
                
                
def nod_yes(times):
    global in_gesture
    sleepTime = 0.03
    for j in range(0,times):
        #resetCameraPos()
        for i in range(0,6):
            time.sleep(sleepTime)
            video_dir.move_decrease_y()
        for i in range(0,9):
            time.sleep(sleepTime)
            video_dir.move_increase_y()
        for i in range(0,3):
            time.sleep(sleepTime)
            video_dir.move_decrease_y()
    in_gesture = False
    return

def nod_no(times):
    global in_gesture
    sleepTime = 0.03
    for j in range(0,times):
        #resetCameraPos()
        for i in range(0,6):
            time.sleep(sleepTime)
            video_dir.move_decrease_x()
        for i in range(0,9):
            time.sleep(sleepTime)
            video_dir.move_increase_x()
        for i in range(0,3):
            time.sleep(sleepTime)
            video_dir.move_decrease_x()
    in_gesture = False

def circle_head(times):
    global in_gesture
    sleepTime = 0.03
    for j in range(0,times):
        #resetCameraPos()
        for i in range(0,2):
            time.sleep(sleepTime)
            video_dir.move_decrease_y()
        for i in range(0,5):
            time.sleep(sleepTime)
            video_dir.move_increase_x()
            video_dir.move_increase_y()
        for i in range(0,5):
            time.sleep(sleepTime)
            video_dir.move_decrease_x()
            video_dir.move_increase_y()
        for i in range(0,5):
            time.sleep(sleepTime)
            video_dir.move_decrease_x()
            video_dir.move_decrease_y()
        for i in range(0,5):
            time.sleep(sleepTime)
            video_dir.move_increase_x()
            video_dir.move_decrease_y()
        for i in range(0,2):
            time.sleep(sleepTime)
            video_dir.move_increase_y()
    in_gesture = False

def look_left():
    global in_gesture
    sleepTime = 0.03
    for i in range(0,5):
        time.sleep(sleepTime)
        video_dir.move_decrease_x()
    time.sleep(1)
    for i in range(0,5):
        time.sleep(sleepTime)
        video_dir.move_increase_x()
    in_gesture = False

def look_right():
    global in_gesture
    sleepTime = 0.03
    for i in range(0,5):
        time.sleep(sleepTime)
        video_dir.move_increase_x()
    time.sleep(1)
    for i in range(0,5):
        time.sleep(sleepTime)
        video_dir.move_decrease_x()
    in_gesture = False

def look_up():
    global in_gesture
    sleepTime = 0.03
    for i in range(0,5):
        time.sleep(sleepTime)
        video_dir.move_decrease_y()
    time.sleep(1)
    for i in range(0,5):
        time.sleep(sleepTime)
        video_dir.move_increase_y()
    in_gesture = False

def look_down():
    global in_gesture
    sleepTime = 0.03
    for i in range(0,5):
        time.sleep(sleepTime)
        video_dir.move_increase_y()
    time.sleep(1)
    for i in range(0,5):
        time.sleep(sleepTime)
        video_dir.move_decrease_y()
    in_gesture = False

def dance(seconds):
    global in_gesture
    t_start = time.time()
    while time.time() < t_start + seconds/2:
        motor.backward()
    motor.stop()
    look_right()
    while time.time() < t_start + seconds:
        motor.forward()
    look_left()
    in_gesture = False
    
def on_press(key):
    global enableApple
    global enableFollowMode
    global lastChar
    global spd
    currentKey = -1
    try:
        currentKey = key.char
    except Exception:
        currentKey = key

    if (currentKey == 'a'):
        car_dir.turn_left()
    if (currentKey == 'd'):
        car_dir.turn_right()
        
    if(lastChar != -1 and lastChar != 'a' and lastChar != 'd'):
        return
    lastChar = currentKey
    
    if (currentKey == "+" and spd < 100):
        spd += 5
        motor.setSpeed(spd)
    if (currentKey == "-" and spd > 0):
        spd -= 5
        motor.setSpeed(spd)
    if (currentKey == 'w'):
        motor.forward()
    if (currentKey == 's'):
        motor.backward()
    if (currentKey == keyboard.Key.down):
        video_dir.move_increase_y()
    if (currentKey == keyboard.Key.up):
        video_dir.move_decrease_y()
    if (currentKey == keyboard.Key.left):
        video_dir.move_decrease_x()
    if (currentKey == keyboard.Key.right):
        video_dir.move_increase_x()
    if (currentKey == 'y'):
        nod_yes(3)
    if (currentKey == 'n'):
        nod_no(3)
    if (currentKey == 'c'):
        circle_head(1)
    if (currentKey == 'l'):
        look_left()
    if (currentKey == 'r'):
        look_right()
    if (currentKey == 'u'):
        look_up()
    if (currentKey == 'b'):
        look_down()
    if (currentKey == 'o'):
        dance(3)
    if (currentKey == 'z'):
        enableApple = not enableApple
    if (currentKey == 'f'):
        enableFollowMode = not enableFollowMode

        
def resetCameraPos():
    sleepTime = 0.01
    video_dir.move_increase_y()
    time.sleep(sleepTime)
    video_dir.move_increase_y()
    time.sleep(sleepTime)
    video_dir.move_increase_y()
    time.sleep(sleepTime)
    video_dir.move_increase_y()
    time.sleep(sleepTime)
    video_dir.move_increase_y()
    time.sleep(sleepTime)
    video_dir.move_increase_y()
    time.sleep(sleepTime)
    video_dir.move_increase_y()        
    time.sleep(sleepTime)
    video_dir.move_increase_y()
    time.sleep(sleepTime)
    video_dir.move_increase_y()
    time.sleep(sleepTime)
    video_dir.move_increase_y()
    time.sleep(sleepTime)
    video_dir.move_increase_y()

def on_release(key):
    global lastChar
    if key == keyboard.Key.esc:
      # Stop listener
        car_dir.home()
        motor.ctrl(0)
        return False

    currentKey = -1
    try:
        currentKey = key.char
    except Exception:
        currentKey = key

    if currentKey != lastChar:
        return
    lastChar = -1
    if (currentKey == 'a' or currentKey == 'd'):
        car_dir.home()
    motor.ctrl(0)
    
resetCameraPos()
# Collect events until released
def listen():
    print 'listenenting'
    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()
