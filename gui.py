import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from pathlib import Path
from PIL import Image, ImageTk  # For arrow icon, requires pillow
import sys

class CopilotGUI:
    def __init__(self, on_send):
        self.root = tk.Tk()
        self.root.title("AI Copilot Prompt")
        self.root.geometry("420x320")
        self.root.resizable(False, False)
        self.on_send = on_send

        # --- Prompt Label ---
        label = ttk.Label(self.root, text="Enter your prompt:")
        label.pack(pady=(12, 0), anchor="w", padx=16)

        # --- Multiline Text Box ---
        self.text = tk.Text(self.root, height=10, width=48, font=("Segoe UI", 11))
        self.text.pack(padx=16, pady=(4, 8), fill="x")
        self.text.focus_set()

        # --- Button Frame ---
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=8, padx=16, fill="x")

        # --- Send Button with Arrow Icon ---
        self.arrow_img = self._load_arrow_icon()
        if self.arrow_img is not None:
            self.send_btn = ttk.Button(btn_frame, text="Send", image=self.arrow_img, compound="right", command=self._on_send)
        else:
            self.send_btn = ttk.Button(btn_frame, text="Send", command=self._on_send)
        self.send_btn.pack(side="right")

        # Bind Ctrl+Enter to send
        self.root.bind('<Control-Return>', lambda e: self._on_send())

        # Position the window in the bottom-right corner
        self.position_bottom_right()

    def _load_arrow_icon(self):
        # Simple right arrow icon (drawn with Pillow)
        try:
            from PIL import Image, ImageDraw
            img = Image.new('RGBA', (20, 20), (255, 255, 255, 0))
            draw = ImageDraw.Draw(img)
            draw.polygon([(5, 5), (15, 10), (5, 15)], fill=(60, 60, 60))
            return ImageTk.PhotoImage(img)
        except Exception:
            return None

    def _on_send(self):
        prompt = self.text.get("1.0", tk.END).strip()
        if not prompt:
            messagebox.showinfo("Empty Prompt", "Please enter a prompt.")
            return
        self.on_send(prompt)
        self.text.delete("1.0", tk.END)

    def set_disabled(self, disabled=True):
        state = tk.DISABLED if disabled else tk.NORMAL
        self.text.config(state=state)
        self.send_btn.config(state=state)

    def position_bottom_right(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = screen_width - width - 20
        y = screen_height - height - 60
        self.root.geometry(f"+{x}+{y}")

    def mainloop(self):
        self.root.mainloop() 