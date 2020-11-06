#TODO: create 
from constantes import *
from buttons import *
from encoder import RotaryEncoder, debit_event, volume_event
from gpiozero import Button
from time import sleep
from subprocess import run

def Main_loop():
    button_alim = Button(GPIO_ALIM)
    button_cancel = Button(GPIO_CANCEL, )
    button_back = Button(GPIO_BACK_BUTTON)
    button_forward = Button(GPIO_FORWARD_BUTTON)
    button_capture = Button(GPIO_CAPTURE)
    button_play = Button(GPIO_PLAY)
    volume_encoder = RotaryEncoder(DT_VOLUME, CLK_VOLUME, True)
    debit_encoder = RotaryEncoder(DT_DEBIT, CLK_DEBIT, True)
    button_alim.when_pressed = alim_event
    button_cancel.when_pressed = cancel_event
    button_back.when_pressed = back_event
    button_forward.when_pressed = forward_event
    button_play.when_pressed = play_event
    button_capture.when_pressed = capture_event
    volume_encoder.when_rotated = volume_event
    debit_encoder.when_rotated = debit_event
    
    while True:
        sleep(1)
        
if __name__ == '__main__':
    try:
        run(['sudo','killall', 'orca'])
        sleep(0.1)
        Main_loop()
    except Exception as e:
        print(e)
