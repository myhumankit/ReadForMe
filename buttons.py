import RPi.GPIO as GPIO
import time
from subprocess import run, Popen
from send_shortcuts import send_shortcut

is_play = False

cur_process = None

def alim_event():
    print("alim button pressed")
    run(['sudo','shutdown','now'])

def cancel_event():
    print("cancel button pressed")
    global cur_process
    if cur_process:
        print("kill ok")
        cur_process.terminate()
        cur_process = None
        run(['sudo','killall','orca'])
        #run(['sudo','killall','zenity'])
        #run(['sudo','killall','aplay'])
   
def back_event():
    print("back button pressed")
    send_shortcut("KP_Down")

def forward_event():
    print("forward button pressed")
    send_shortcut("KP_Up")
    
def capture_event():
    global cur_process
    print("capture button pressed")
    #run(['orca','--replace','&'])
    #time.sleep(3)
    #send_shortcut('Insert+s')
    #time.sleep(0.3)
    cur_process = Popen(['./OCRSCan'])
    
def play_event():
    global is_play
    print("play/pause button pressed")
    if is_play:
        print("pause")
        send_shortcut('ctrl')
        is_play = False
    else:
        print("play")
        send_shortcut('KP_Add')
        is_play = True
