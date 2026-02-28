import time
import threading 
from pynput.mouse import Controller, Button
from pynput.keyboard import GlobalHotKeys

LEFT_CLICK_INTERVAL = 1.0

clicking = False
mouse = Controller()

def clicker():
    while True:
        if clicking:
            mouse.click(Button.left, 1)
            time.sleep(LEFT_CLICK_INTERVAL)
        else:
            time.sleep(0.01)

def toggle_clicking():
    """Toggle auto-clicker on or off when toggle hotkey is pressed."""
    global clicking
    clicking = not clicking
    print(f"Auto-clicker active: {clicking}")

def exit_script():
    """Exit auto-clicker when exit hotkey is pressed."""
    print("Exiting script...")
    return False

click_thread = threading.Thread(target=clicker, daemon=True)
click_thread.start()

hotkeys = {
    '<ctrl>+<shift>+t': toggle_clicking,
    '<ctrl>+<shift>+x': exit_script
}

print("Listening for hotkeys...")
print("  Press Ctrl+Shift+T to Toggle")
print("  Press Ctrl+Shift+X to Exit")

with GlobalHotKeys(hotkeys) as listener:
    listener.join()
