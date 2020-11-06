import RPi.GPIO as GPIO
import time
from subprocess import run
from send_shortcuts import send_shortcut

is_play = False

def alim_event():
    print("alim button pressed")
    run(['sudo','shutdown','now'])

def cancel_event():
    print("cancel button pressed")
    run(['killall','python3'])
    
def back_event():
    print("back button pressed")
    send_shortcut("KP_Down")

def forward_event():
    print("forward button pressed")
    send_shortcut("KP_Up")
    
def capture_event():
    print("capture button pressed")
    run(['./../document-scanner/orcscan'])
    
def play_event():
    global is_play
    print("play/pause button pressed")
    if is_play:
        print("pause")
        is_play = False
    else:
        print("play")
        is_play = True
