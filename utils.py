from PIL import Image, ImageEnhance
from rembg import remove
from google import genai
from google.genai import types
from io import BytesIO
import os
class ImageState:
	def __init__(self):
		self.original: Image.Image | None = None
		self.current: Image.Image | None = None
		self.current_without_enhancements: Image.Image | None = None
		self.enhancement_mode_enabled: bool | None = None
		self.enhancement_values = {
			"brightness": 1,
			"contrast": 1,
			"sharpness": 1
		}
		self.file_path: str | None = None

class ImageProcessor:
	@staticmethod
	def flip_horizontal(img: Image.Image) -> Image.Image:
			return img.transpose(Image.FLIP_LEFT_RIGHT)

	@staticmethod
	def rotate(img: Image.Image, degrees: int) -> Image.Image:
			return img.rotate(degrees, expand=True)

	@staticmethod
	def crop(img: Image.Image, box: tuple) -> Image.Image:
			return img.crop(box)

	@staticmethod
	def adjust_brightness(img: Image.Image, factor: float) -> Image.Image:
			return ImageEnhance.Brightness(img).enhance(factor)

	@staticmethod
	def adjust_contrast(img: Image.Image, factor: float) -> Image.Image:
			return ImageEnhance.Contrast(img).enhance(factor)

	@staticmethod
	def adjust_sharpness(img: Image.Image, factor: float) -> Image.Image:
			return ImageEnhance.Sharpness(img).enhance(factor)

	@staticmethod
	def remove_background(img: Image.Image) -> Image.Image:
		return remove(img)
	
	@staticmethod
	def describe_image(img: Image.Image) -> str:
		fmt = img.format or "PNG"
		api_key = os.getenv("GOOGLE_API_KEY")
		mime_type = f"image/{fmt.lower()}"
		
		buffer = BytesIO()
		img.save(buffer, format=fmt)
		image_bytes = buffer.getvalue()

		client = genai.Client(api_key=api_key)
		response = client.models.generate_content(
			model='gemini-3-flash-preview',
			contents=[
				types.Part.from_bytes(
					data=image_bytes,
					mime_type=mime_type,
				),
				'Describe the content of this image in short. Max 5 sentences.'
			]
		)

		return response.text

class UndoManager:
	def __init__(self, max_history=20):
			self._stack: list[dict] = []
			self._max = max_history

	def push(self, img: Image.Image):
			"""Push a state onto undo stack.
			
			Args:
				img: The image to save
			"""
			state = {
				"image": img.copy(),
			}
			self._stack.append(state)
			if len(self._stack) > self._max:
					self._stack.pop(0)
	


	def undo(self) -> tuple[Image.Image] | None:
			"""Pop from undo stack.
			
			Returns:
				Tuple of (image) or None if stack is empty
			"""
			if not self._stack:
				return None
			state = self._stack.pop()
			return (state["image"])

	def can_undo(self) -> bool:
			return len(self._stack) > 0
    