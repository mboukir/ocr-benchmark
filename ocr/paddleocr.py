from paddleocr import PaddleOCR as pocr
from ocr.base import BaseOCR

class PaddleOCR(BaseOCR):
    def initialize(self):
        self.paddle_ocr = pocr(
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=False,
            lang="en")

    def process_image(self, image_path):
        print("!")
        results = self.paddle_ocr.ocr(image_path)
        print("!")
        return results

    def cleanup(self):
        pass
        # del self.paddle_ocr