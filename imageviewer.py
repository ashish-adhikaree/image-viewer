import threading
import tkinter as tk
from tkinter import filedialog
from turtle import done
from PIL import Image
from utils import ImageState, ImageProcessor, UndoManager
from toolbar import BUTTON_STYLE, Toolbar
from canvas import CanvasView
from sidebar import Sidebar
from constant import FONT, BLACK_COLOR, YELLOW_COLOR
class ImageViewer(tk.Frame):
	def __init__(self, parent, controller):
			super().__init__(parent)

			# instantiate all services
			self.state = ImageState()
			self.processor = ImageProcessor()
			self.undo_mgr = UndoManager()

			self._build_ui()

	def _build_ui(self):
			callbacks = {
					"open":    self.open_image,
					"save":    self.save_image,
					"flip_h":  self.flip_horizontal,
					"rotate":  self.rotate_90,
					"crop":    self.enable_crop,
					"undo":    self.undo,
					"toggle_enhance_mode": self.toggle_enhance_mode,
					"remove_bg": self.remove_background,
					"describe": self.describe_image
			}

			self.description = tk.Frame(self, padx=20, pady=20, bg=BLACK_COLOR)
			self.description.place(relx=0.95, rely=0.1, anchor="ne")

			self.description_label = tk.Label(self.description, text="", font=FONT, bg=BLACK_COLOR, fg="#ffffff", wraplength=300, justify="left")
			self.description_label.pack()

			tk.Button(self.description, text="Close", command=self.hide_description, **BUTTON_STYLE).pack(pady=(10,0))
			
			self.sidebar = Sidebar(self, on_change=self._apply_enhancements, reset_callback = self._reset_enhancements)
			self.sidebar.place(relx=0.95, rely=0.5, anchor="e")
	
			self.canvas_view = CanvasView(self)
			self.canvas_view.pack(side="left", fill="both", expand=True)

			self.toolbar = Toolbar(self, callbacks)
			self.toolbar.place(relx=0.5, y=10, anchor="n")

	def toggle_enhance_mode(self):
		if (self.state.enhancement_mode_enabled):
			self.state.enhancement_mode_enabled = False
			self.toolbar.toggle_state("toggle_enhance_mode", enabled=False)
			self._hide_sidebar()
		else:
			self.state.enhancement_mode_enabled = True
			self.toolbar.toggle_state("toggle_enhance_mode", enabled=True)
			self._show_sidebar()
	
	def _show_sidebar(self):
		self.sidebar.tkraise()

	def _hide_sidebar(self):
		self.sidebar.lower()

	def _apply_enhancements(self, key, value):
			if not self.state.current_without_enhancements:
					return
			
			img = self.state.current_without_enhancements.copy()
			
			self.state.enhancement_values[key] = value

			img = self.processor.adjust_brightness(img, self.state.enhancement_values["brightness"])
			img = self.processor.adjust_contrast(img, self.state.enhancement_values["contrast"])
			img = self.processor.adjust_sharpness(img, self.state.enhancement_values["sharpness"])
	
			self.state.current = img
			
			self.canvas_view.display(img)

	def _reset_enhancements(self):
		self.state.enhancement_values = {
			"brightness": 1,
			"contrast": 1,
			"sharpness": 1
		}
		self.sidebar.set_slider_value("brightness", 1.0)
		self.sidebar.set_slider_value("contrast", 1.0)
		self.sidebar.set_slider_value("sharpness", 1.0)

		self.canvas_view.display(self.state.current)

	def describe_image(self):
		if not self.state.current:
			return
		
		self.toolbar.toggle_state("describe", enabled=True)
		self.display_description("Generating description...")

		description = self.processor.describe_image(self.state.current)
		self.display_description(description)

		self.toolbar.toggle_state("describe", enabled=False)

	def display_description(self, description):
		self.description_label.config(text=description)
		self.description.tkraise()
		self.description_label.update_idletasks()

	def hide_description(self):
		self.description.lower()
		self.description_label.config(text="")

	def open_image(self, path=None):
			if not path:
				path = filedialog.askopenfilename()

			if path:
					self.state.original = Image.open(path)
					self.state.current = self.state.original.copy()
					self.state.current_without_enhancements = self.state.original.copy()
					
					self._reset_enhancements()
				
	def flip_horizontal(self):
			if not self.state.current: return

			# Save current state for undo
			self.undo_mgr.push(self.state.current)

			#Apply horizontal flip
			flipped = self.processor.flip_horizontal(self.state.current)

			#Update state
			self.state.current = flipped
			
			#Update current_without_enhancements for enhancements to apply on top of flipped image
			self.state.current_without_enhancements = flipped.copy()

			#Display flipped image
			self.canvas_view.display(self.state.current)

	def remove_background(self):
			if not self.state.current: return

			# Save current state for undo
			self.undo_mgr.push(self.state.current)

			#Apply background removal
			bg_removed = self.processor.remove_background(self.state.current)

			#Update state
			self.state.current = bg_removed
			
			#Update current_without_enhancements for enhancements to apply on top of bg removed image
			self.state.current_without_enhancements = bg_removed.copy()

			#Display bg removed image
			self.canvas_view.display(self.state.current)

	def rotate_90(self):
		if not self.state.current:
			return
		
		# Save current state for undo
		self.undo_mgr.push(self.state.current)

		# Apply rotation
		rotated = self.processor.rotate(self.state.current, 90)

		# Update state
		self.state.current = rotated

		#Update current_without_enhancements for enhancements to apply on top of rotated image
		self.state.current_without_enhancements = rotated.copy()

		# Display rotated image
		self.canvas_view.display(self.state.current)
   
	def undo(self):
			result = self.undo_mgr.undo()
			if result:
					img = result
					self.state.current = img
					self.state.current_without_enhancements = img
	
					self.canvas_view.display(img)
	
	def save_image(self):
		if not self.state.current: return

		path = filedialog.asksaveasfilename(
				defaultextension=".png",
				filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("All files", "*.*")]
		)

		if path:
				self.state.current.save(path)

	def enable_crop(self):
		if not self.state.current: return
			
		# Enable crop mode on canvas
		self.toolbar.toggle_state("crop", enabled=True)
		self.canvas_view.enable_crop_mode(self._on_crop_complete)

	def _on_crop_complete(self, crop_box):
		"""Callback when crop is completed."""
		if not self.state.current:
			return
		
		self.toolbar.toggle_state("crop", enabled=False)

		# Save current state for undo
		self.undo_mgr.push(self.state.current)

		# Apply crop
		cropped = self.processor.crop(self.state.current, crop_box)
		
		# Update state
		self.state.current = cropped
		
		#Update current_without_enhancements for enhancements to apply on top of cropped image
		self.state.current_without_enhancements = cropped.copy()

		# Disable crop mode
		self.canvas_view.disable_crop_mode()
		
		# Display cropped image
		self.canvas_view.display(cropped)
