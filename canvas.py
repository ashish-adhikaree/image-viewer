from PIL import Image, ImageTk
import tkinter as tk
from constant import BLACK_COLOR

class CanvasView(tk.Frame):
		def __init__(self, parent):
				super().__init__(parent)
				self.canvas = tk.Canvas(self, bg=BLACK_COLOR)
				self.canvas.pack(fill="both", expand=True)
				self._tk_image = None  # must hold reference or GC kills it!

				# crop state
				self._crop_start = None
				self._crop_rect = None
				self._crop_mode = False
				self._on_crop_complete = None
				self._image_position = (0, 0)  # (x_center, y_center)
				self._displayed_img = None  # keep reference to displayed image
				self._original_img = None  # keep reference to original unscaled image
				

		def enable_crop_mode(self, on_crop_complete):
				"""Enable crop mode and set callback for when crop is complete."""
				self.canvas.config(cursor="sizing")
				self._crop_mode = True
				self._on_crop_complete = on_crop_complete
				self.canvas.bind("<Button-1>", self._on_crop_start)
				self.canvas.bind("<B1-Motion>", self._on_crop_drag)
				self.canvas.bind("<ButtonRelease-1>", self._on_crop_end)

		def disable_crop_mode(self):
				"""Disable crop mode."""
				self._crop_mode = False
				self._on_crop_complete = None
				self.canvas.unbind("<Button-1>")
				self.canvas.unbind("<B1-Motion>")
				self.canvas.unbind("<ButtonRelease-1>")
				if self._crop_rect:
					self.canvas.delete(self._crop_rect)
					self._crop_rect = None

		def _on_crop_start(self, event):
				"""Handle crop start."""
				self._crop_start = (event.x, event.y)
				if self._crop_rect:
					self.canvas.delete(self._crop_rect)

		def _on_crop_drag(self, event):
				"""Handle crop drag."""
				if not self._crop_start:
					return
				
				x0, y0 = self._crop_start
				x1, y1 = event.x, event.y
				
				# Ensure coordinates are in correct order
				x0, x1 = min(x0, x1), max(x0, x1)
				y0, y1 = min(y0, y1), max(y0, y1)
				
				if self._crop_rect:
					self.canvas.delete(self._crop_rect)
				
				self._crop_rect = self.canvas.create_rectangle(
					x0, y0, x1, y1,
					outline="yellow", width=2
				)

		def _on_crop_end(self, event):
				"""Handle crop end."""
				self.canvas.config(cursor="arrow")
				if not self._crop_start or not self._original_img:
					return
				
				x0, y0 = self._crop_start
				x1, y1 = event.x, event.y
				
				# Ensure coordinates are in correct order
				x0, x1 = min(x0, x1), max(x0, x1)
				y0, y1 = min(y0, y1), max(y0, y1)
				
				# Get original image dimensions
				orig_width, orig_height = self._original_img.size
				
				# Get displayed image dimensions
				display_width, display_height = self._displayed_img.size
				cx, cy = self._image_position  # center of image on canvas
				
				# Calculate image bounds on canvas
				# Image is centered and may be smaller than canvas
				img_left = cx - display_width // 2
				img_top = cy - display_height // 2
				img_right = img_left + display_width
				img_bottom = img_top + display_height
				
				# Clamp selection to image bounds on canvas
				x0 = max(x0, img_left)
				y0 = max(y0, img_top)
				x1 = min(x1, img_right)
				y1 = min(y1, img_bottom)
				
				# Convert canvas coordinates to displayed image coordinates
				disp_x0 = x0 - img_left
				disp_y0 = y0 - img_top
				disp_x1 = x1 - img_left
				disp_y1 = y1 - img_top
				
				# Now scale from displayed image coordinates to original image coordinates
				scale_x = orig_width / display_width if display_width > 0 else 1
				scale_y = orig_height / display_height if display_height > 0 else 1
				
				orig_x0 = int(disp_x0 * scale_x)
				orig_y0 = int(disp_y0 * scale_y)
				orig_x1 = int(disp_x1 * scale_x)
				orig_y1 = int(disp_y1 * scale_y)
				
				# Only process if there's a valid crop area
				if orig_x1 > orig_x0 and orig_y1 > orig_y0:
					crop_box = (orig_x0, orig_y0, orig_x1, orig_y1)
					if self._on_crop_complete:
						self._on_crop_complete(crop_box)
				
				# Clean up crop state
				self._crop_start = None
				if self._crop_rect:
					self.canvas.delete(self._crop_rect)
					self._crop_rect = None

		def display(self, img: Image.Image):
				self._original_img = img  # Store original image		
				cw, ch = self.canvas.winfo_width(), self.canvas.winfo_height()
				img_fit = self._fit_to_canvas(img, cw, ch)
				self._displayed_img = img_fit
				self._tk_image = ImageTk.PhotoImage(img_fit)
				self.canvas.delete("all")
				self._image_position = (cw // 2, ch // 2)
				self.canvas.create_image(cw // 2, ch // 2, image=self._tk_image, anchor="center")

		def _fit_to_canvas(self, img, cw, ch) -> Image.Image:
				img.thumbnail((cw, ch), Image.LANCZOS)
				return img
