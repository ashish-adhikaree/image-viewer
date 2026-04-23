from logging import root
import tkinter as tk
from constant import YELLOW_COLOR, DARK_YELLOW_COLOR, FONT

BUTTON_STYLE = {
    "bg": YELLOW_COLOR,
    "fg": "black",
    "activebackground": DARK_YELLOW_COLOR,
    "activeforeground": "black",
    "font": FONT,
    "relief": tk.FLAT,
		"highlightthickness": 0,
    "bd": 0,
    "padx": 10,
    "pady": 5,
		"cursor": "hand2"
}

class Toolbar(tk.Frame):
	def __init__(self, parent, callbacks: dict):
			super().__init__(parent, bg="#2d2d2d", pady=4)
			self.button_elements = {}

			buttons = [
					("📂 OPEN", "open"),
					("↔ FLIP", "flip_h"),
					("↻° 90", "rotate"),
					("✂ CROP", "crop"),
					("⎌ UNDO", "undo"),
					("REMOVE BG", "remove_bg"),
					("ENHANCE", "toggle_enhance_mode"),
					("DESCRIBE", "describe"),
					("💾 SAVE", "save"),
			]

			for text, key in buttons:
					btn = tk.Button(
							self,
							text=text,
							command=callbacks[key],
							**BUTTON_STYLE,
					)
					btn.pack(side="left", padx=4)
					self.button_elements[key] = btn
		
	def toggle_state(self, btn_key, enabled=True):
		btn = self.button_elements.get(btn_key)
		if btn:
			if enabled:
				btn.config(bg="#000000", fg="white", activebackground="#000000", activeforeground="white")
			else:
				btn.config(bg=BUTTON_STYLE["bg"], fg=BUTTON_STYLE["fg"], activebackground=BUTTON_STYLE["activebackground"], activeforeground=BUTTON_STYLE["activeforeground"])