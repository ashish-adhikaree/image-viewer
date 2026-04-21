import tkinter as tk
from toolbar import BUTTON_STYLE
from constant import YELLOW_COLOR, BLACK_COLOR, DARK_YELLOW_COLOR

class DarkSlider(tk.Frame):
    def __init__(self, parent, label_text, icon_char, initial_val=50):
        super().__init__(parent, bg=BLACK_COLOR, highlightbackground="#3A2B01", 
                         highlightthickness=1, padx=10, pady=10)
        
        # Grid weights for alignment
        self.columnconfigure(2, weight=1)

        # 1. Icon (Using a simple string placeholder for the icon)
        self.icon = tk.Label(self, text=icon_char, fg="white", bg=BLACK_COLOR, 
                             font=("Segoe UI Symbol", 14))
        self.icon.grid(row=0, column=0, padx=(0, 10))

        # 2. Text Label
        self.label = tk.Label(self, text=label_text, fg="white", bg=BLACK_COLOR, 
                              font=("Courier New", 12, "bold"))
        self.label.grid(row=0, column=1, sticky="w", padx=(0, 20))

        # 3. Custom Styled Scale
        self.scale = tk.Scale(self, from_=0, to=100, orient="horizontal",
                              bg=YELLOW_COLOR, 
                              fg=BLACK_COLOR,            
                              troughcolor="#33332d", 
                              highlightthickness=0,
                              activebackground=DARK_YELLOW_COLOR,
                              sliderrelief="flat",
                              sliderlength=15,
                              width=8,
                              bd=0,
                              showvalue=False)
															
        self.scale.set(initial_val)
        self.scale.grid(row=0, column=2, sticky="ew")


class Sidebar(tk.Frame):
	def __init__(self, parent, on_change, reset_callback):
			super().__init__(parent, bg="#252525", padx=10)
			self._on_change = on_change
			self._sliders = {}
			
			self._add_slider("Brightness", "brightness", "☼", 1.0)
			self._add_slider("Contrast",   "contrast",   "◐", 1.0)
			self._add_slider("Sharpness",  "sharpness",  "◢", 1.0)
			tk.Button(self, text="Reset", command=reset_callback, **BUTTON_STYLE).pack(fill="x", pady=(10,0))

	def _add_slider(self, label, key, icon, default):
			s = DarkSlider(self, label, icon, int(default * 50))
			s.scale.config(command=lambda v, k=key: self._on_change(k, float(v) / 50))
			s.pack(fill="x", pady=5)
			self._sliders[key] = s

	def set_slider_value(self, key, value):
			"""Set slider value without triggering callback."""
			if key in self._sliders:
				self._sliders[key].scale.set(int(value * 50))
        
 