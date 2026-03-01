import time
import threading
from pynput.mouse import Controller, Button
from pynput.keyboard import GlobalHotKeys

LEFT_CLICK_INTERVAL = 1.0
ENABLE_RIGHT_HOLD = False

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
    """Toggle auto-clicker on or off."""
    global clicking
    clicking = not clicking

    if ENABLE_RIGHT_HOLD:
        if clicking:
            mouse.press(Button.right)
        else:
            mouse.release(Button.right)
  
    print(f"Auto-clicker: {'RUNNING' if clicking else 'STOPPED'}")

def toggle_right_hold():
    """Toggle hold right-click on or off."""
    global ENABLE_RIGHT_HOLD
    ENABLE_RIGHT_HOLD = not ENABLE_RIGHT_HOLD

    if clicking:
        if ENABLE_RIGHT_HOLD:
            mouse.press(Button.right)
        else:
            mouse.release(Button.right)

    print(f"Right-Hold mode: {'ON' if ENABLE_RIGHT_HOLD else 'OFF'}")

def exit_script():
    """Exit auto-clicker."""
    print("Exiting script...")
    if clicking and ENABLE_RIGHT_HOLD:
        mouse.release(Button.right)
    return False

click_thread = threading.Thread(target=clicker, daemon=True)
click_thread.start()

hotkeys = {
    '<ctrl>+<shift>+t': toggle_clicking,
    '<ctrl>+<shift>+r': toggle_right_hold,
    '<ctrl>+<shift>+x': exit_script
}

print("--- Auto Clicker ---")
print("Listening for hotkeys...")
print("  Press `Ctrl+Shift+T` to toggle left-clicking.")
print("  Press `Ctrl+Shift+R` to toggle right-hold mode.")
print("  Press `Ctrl+Shift+X` to exit.")
print(f"  Right Hold feature is {'ON' if ENABLE_RIGHT_HOLD else 'OFF'}\n")

with GlobalHotKeys(hotkeys) as listener:
    listener.join()
