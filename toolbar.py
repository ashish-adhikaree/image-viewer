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

        buttons = [
            ("⤓ OPEN", "open"),
            ("⎙ SAVE", "save"),
            ("↔ FLIP", "flip_h"),
            ("↻ 90°", "rotate"),
            ("✂ CROP", "crop"),
            ("↩ UNDO", "undo"),
            ("REMOVE BG", "remove_bg"),
            ("ENHANCE", "toggle_enhance_mode")
        ]

        for text, key in buttons:
            tk.Button(
                self,
                text=text,
                command=callbacks[key],
                **BUTTON_STYLE
            ).pack(side="left", padx=4)