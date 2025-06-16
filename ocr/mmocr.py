from mmocr.apis import MMOCRInferencer

from ocr.base import BaseOCR

class MMOCR(BaseOCR):
    def initialize(self):
        # Load models into memory
        self.mmocr = MMOCRInferencer(det='DBNet', rec='SAR')
        
    def process_image(self, image_path):
        results = self.mmocr(image_path, print_result=False)
        return results

    def cleanup(self):
        del self.mmocr