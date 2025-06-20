import pyautogui
import tkinter as tk
import time
import threading
import sys

# For click-through on Windows
if sys.platform == 'win32':
    import ctypes
    from ctypes import windll, wintypes

# Function to update the label with the current mouse position
def update_position():
    while True:
        x, y = pyautogui.position()
        position_str = f'X: {x:4}  Y: {y:4}'
        label_var.set(position_str)
        # Move window to top right (in case of screen resize)
        root.update_idletasks()
        screen_width = root.winfo_screenwidth()
        window_width = root.winfo_width()
        root.geometry(f'+{screen_width - window_width - 10}+10')
        time.sleep(0.05)

root = tk.Tk()
root.overrideredirect(True)  # Remove window borders
root.attributes('-topmost', True)  # Always on top
root.attributes('-alpha', 0.7)  # Semi-transparent

label_var = tk.StringVar()
label = tk.Label(root, textvariable=label_var, font=('Consolas', 16), bg='black', fg='lime')
label.pack(ipadx=10, ipady=5)

# Initial position at top right
root.update_idletasks()
screen_width = root.winfo_screenwidth()
window_width = root.winfo_width()
root.geometry(f'+{screen_width - window_width - 10}+10')

# Make window click-through on Windows
if sys.platform == 'win32':
    hwnd = windll.user32.GetParent(root.winfo_id())
    GWL_EXSTYLE = -20
    WS_EX_LAYERED = 0x80000
    WS_EX_TRANSPARENT = 0x20
    style = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    style |= WS_EX_LAYERED | WS_EX_TRANSPARENT
    windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)

# Start the update thread
t = threading.Thread(target=update_position, daemon=True)
t.start()

try:
    root.mainloop()
except KeyboardInterrupt:
    pass