import tkinter as tk
from filepicker import FilePicker
from imageviewer import ImageViewer
from tkinter import filedialog

class App():
	def __init__(self, root: tk.Tk):
		self.root = root
		self.root.title("Image Editor")
		self.root.geometry("1000x650")

		self.container = tk.Frame(self.root)
		self.container.pack(fill="both", expand=True)

		self.frames = {}

		self._add_pages()
		self.show_frame("FilePicker")

	def _add_pages(self):
		controller = {
			"open_file": self._open_file
		}

		self.container.rowconfigure(0, weight=1)
		self.container.columnconfigure(0, weight=1)
		
		for Page in (FilePicker, ImageViewer):
			page_name = Page.__name__
			
			frame = Page(self.container, controller)

			self.frames[page_name] = frame

			frame.grid(row=0, column=0, sticky="nsew")

	def show_frame(self, page_name):
		frame = self.frames[page_name]
		frame.tkraise()

	def _open_file(self):
		path = filedialog.askopenfilename()
		if path:
			imageviewer = self.frames["ImageViewer"]	

			imageviewer.open_image(path, show_frame=True)


