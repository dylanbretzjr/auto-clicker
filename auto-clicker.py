import time
import threading
import tkinter as tk
from pynput.mouse import Controller, Button
from pynput.keyboard import GlobalHotKeys, Listener

# --- Configuration ---

LEFT_CLICK_INTERVAL = 1.5
ENABLE_RIGHT_HOLD = False

clicking = False
mouse = Controller()

# --- Core logic ---

def clicker():
    """Background thread to handle clicking."""
    global LEFT_CLICK_INTERVAL
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
  
    status_var.set("RUNNING" if clicking else "STOPPED")
    status_label.config(fg="green" if clicking else "red")

def toggle_right_hold():
    """Toggle hold right-click on or off."""
    global ENABLE_RIGHT_HOLD
    ENABLE_RIGHT_HOLD = not ENABLE_RIGHT_HOLD

    if clicking:
        if ENABLE_RIGHT_HOLD:
            mouse.press(Button.right)
        else:
            mouse.release(Button.right)

    right_hold_var.set("ON" if ENABLE_RIGHT_HOLD else "OFF")
    right_hold_label.config(fg="green" if ENABLE_RIGHT_HOLD else "red")

def update_interval(*args):
    """Dynamically updates the click speed when typed into the GUI."""
    global LEFT_CLICK_INTERVAL
    try:
        LEFT_CLICK_INTERVAL = float(interval_var.get())
    except ValueError:
        pass

def exit_script():
    """Exit auto-clicker."""
    if clicking and ENABLE_RIGHT_HOLD:
        mouse.release(Button.right)
    root.after(0, root.destroy)
    raise Listener.StopException

# --- GUI setup ---

root = tk.Tk()
root.title("Auto-Clicker")
root.geometry("300x300")
root.attributes("-topmost", True)

font_title = ("Helvetica", 16, "bold")
font_normal = ("Helvetica", 12)

tk.Label(root, text="Auto-Clicker", font=font_title).pack(pady=10)

# Interval input
interval_frame = tk.Frame(root)
interval_frame.pack(pady=5)
tk.Label(interval_frame, text="Click Interval (seconds):", font=font_normal).pack(side=tk.LEFT)

interval_var = tk.StringVar(value=str(LEFT_CLICK_INTERVAL))
interval_var.trace_add("write", update_interval)
tk.Entry(interval_frame, textvariable=interval_var, width=5, justify="center").pack(side=tk.LEFT, padx=5)

# Status variables
status_var = tk.StringVar(value="STOPPED")
right_hold_var = tk.StringVar(value="OFF")

tk.Label(root, text="Status:", font=font_normal).pack(pady=(15, 0))
status_label = tk.Label(root, textvariable=status_var, font=font_title, fg="red")
status_label.pack()

tk.Label(root, text="Right-Hold Mode:", font=font_normal).pack(pady=(10, 0))
right_hold_label = tk.Label(root, textvariable=right_hold_var, font=font_title, fg="red")
right_hold_label.pack()

# Hotkey instructions
instructions = (
    "Hotkeys:\n"
    "  `Ctrl+Shift+T`: Toggle Left-Clicking\n"
    "  `Ctrl+Shift+R`: Toggle Right-Hold\n"
    "  `Ctrl+Shift+X`: Exit"
)

tk.Label(root, text=instructions, font=font_normal, justify="left").pack(pady=15)

# --- Start background threads ---

click_thread = threading.Thread(target=clicker, daemon=True)
click_thread.start()

hotkeys = {
    '<ctrl>+<shift>+t': toggle_clicking,
    '<ctrl>+<shift>+r': toggle_right_hold,
    '<ctrl>+<shift>+x': exit_script
}

listener = GlobalHotKeys(hotkeys)
listener.start()

# Start GUI loop
root.mainloop()
