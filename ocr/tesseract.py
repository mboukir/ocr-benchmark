import pytesseract
from PIL import Image
from ocr.base import BaseOCR

class TesseractOCR(BaseOCR):
    def initialize(self):
        pass  # Tesseract requires no special initialization

    def process_image(self, image_path):
        image = Image.open(image_path)
        return pytesseract.image_to_string(image, lang='fra')

    def cleanup(self):
        pass  # No cleanup required for Tesseract