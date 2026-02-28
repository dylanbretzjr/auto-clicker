import time
import threading 
from pynput.mouse import Controller, Button
from pynput.keyboard import Listener, KeyCode

LEFT_CLICK_INTERVAL = 1.0

TOGGLE_KEY = KeyCode(char="*")

clicking = False
mouse = Controller()

def clicker():
    while True:
        if clicking:
            mouse.click(Button.left, 1)
            time.sleep(LEFT_CLICK_INTERVAL)

def toggle_event(key):
    if key == TOGGLE_KEY:
        global clicking
        clicking = not clicking

click_thread = threading.Thread(target=clicker)
click_thread.start()

with Listener(on_press=toggle_event) as listener:
    listener.join()
