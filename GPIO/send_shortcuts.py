from subprocess import run

def send_shortcut(key_sequence):
    run(['xdotool','key', key_sequence])