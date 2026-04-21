import tkinter as tk
from toolbar import BUTTON_STYLE
from constant import YELLOW_COLOR
from constant import BLACK_COLOR, FONT_FAMILY

class FilePicker(tk.Frame):
	def __init__(self, parent, controller):
			super().__init__(parent, bg=BLACK_COLOR)
			self.controller = controller
			self._build_ui()

	def _build_ui(self):
			tk.Label(self, text="[SIMPLE IMAGE VIEWER & EDITOR]", font=(FONT_FAMILY, 20, "bold"), fg=YELLOW_COLOR, bg=BLACK_COLOR).pack(padx=4, pady=(72, 24))

			tk.Button(
						self,
						text="⤓ OPEN IMAGE",
						command=self.controller["open_file"],
						**BUTTON_STYLE
				).pack(padx=4)

