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

def sync_mouse_state():
    """Ensure mouse state matches toggle settings."""
    if clicking and ENABLE_RIGHT_HOLD:
        mouse.press(Button.right)
    else:
        mouse.release(Button.right)

def update_ui():
    """Update GUI elements based on current state."""
    if clicking:
        click_toggle_btn.config(text="ON", fg="green")
    else:
        click_toggle_btn.config(text="OFF", fg="red")

    if ENABLE_RIGHT_HOLD:
        right_hold_toggle_btn.config(text="ON", fg="green")
    else:
        right_hold_toggle_btn.config(text="OFF", fg="red")

def toggle_clicking():
    """Toggle auto-clicker on or off."""
    global clicking
    clicking = not clicking

    sync_mouse_state()
    root.after(0, update_ui)

def gui_toggle_clicking():
    """Toggle auto-clicker via GUI button with 3-second delay."""
    if not clicking:
        click_toggle_btn.config(text="3...", fg="orange")
        root.after(1000, lambda: click_toggle_btn.config(text="2...", fg="orange"))
        root.after(2000, lambda: click_toggle_btn.config(text="1...", fg="orange"))
        root.after(3000, toggle_clicking)
    else:
        toggle_clicking()

def toggle_right_hold():
    """Toggle hold right-click on or off."""
    global ENABLE_RIGHT_HOLD
    ENABLE_RIGHT_HOLD = not ENABLE_RIGHT_HOLD

    sync_mouse_state()
    root.after(0, update_ui)

def update_interval(*args):
    """Update click interval from GUI input."""
    global LEFT_CLICK_INTERVAL
    try:
        val = float(interval_var.get())
        if val > 0:
            LEFT_CLICK_INTERVAL = val
    except ValueError:
        pass

def exit_script():
    """Exit auto-clicker."""
    global clicking, ENABLE_RIGHT_HOLD
    clicking = False
    ENABLE_RIGHT_HOLD = False

    sync_mouse_state()
    root.after(0, root.destroy)
    raise Listener.StopException

# --- GUI setup ---

root = tk.Tk()
root.title("Auto-Clicker")
root.geometry("400x300")
root.attributes("-topmost", True)

font_title = ("Helvetica", 18, "bold")
font_button = ("Helvetica", 16, "bold")
font_normal = ("Helvetica", 14)

tk.Label(root, text="Minecraft AFK Auto-Clicker", font=font_title).pack(pady=(15, 0))

# Control frame
control_frame = tk.Frame(root)
control_frame.pack(pady=15)

# Interval input
tk.Label(control_frame, text="Left-click interval (seconds):", font=font_normal).grid(row=0, column=0, sticky="e", padx=10, pady=5)
interval_var = tk.StringVar(value=str(LEFT_CLICK_INTERVAL))
interval_var.trace_add("write", update_interval)
tk.Entry(control_frame, textvariable=interval_var, width=5, justify="center", font=font_normal).grid(row=0, column=1, sticky="w", padx=10, pady=5)

# Clicker toggle
tk.Label(control_frame, text="Toggle clicker:", font=font_normal).grid(row=1, column=0, sticky="e", padx=10, pady=5)
click_toggle_btn = tk.Button(control_frame, text="OFF", fg="red", font=font_button, width=4, command=gui_toggle_clicking)
click_toggle_btn.grid(row=1, column=1, sticky="w", padx=10, pady=5)

# Right-hold toggle
tk.Label(control_frame, text="Toggle right-hold:", font=font_normal).grid(row=2, column=0, sticky="e", padx=10, pady=5)
right_hold_toggle_btn = tk.Button(control_frame, text="OFF", fg="red", font=font_button, width=4, command=toggle_right_hold)
right_hold_toggle_btn.grid(row=2, column=1, sticky="w", padx=10, pady=5)

# Separator
tk.Frame(root, height=1, bg="#444444").pack(fill=tk.X, padx=30)

# Hotkey instructions
instructions = (
    "Hotkeys:\n"
    "Ctrl+Shift+T — Toggle clicker\n"
    "Ctrl+Shift+R — Toggle right-hold\n"
    "Ctrl+Shift+X — Exit"
)

tk.Label(root, text=instructions, font=font_normal, justify="left").pack(pady=(15, 5))

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
