import easyocr
from ocr.base import BaseOCR

class EasyOCR(BaseOCR):
    def initialize(self):
        self.reader = easyocr.Reader(['fr'], gpu=False)

    def process_image(self, image_path):
        return self.reader.readtext(image_path, detail=0)

    def cleanup(self):
        del self.reader