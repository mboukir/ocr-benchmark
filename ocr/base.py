import abc

class BaseOCR(abc.ABC):
    @abc.abstractmethod
    def initialize(self):
        """Initialize the OCR engine."""
        pass

    @abc.abstractmethod
    def process_image(self, image_path):
        """Process an image and return the extracted text."""
        pass

    @abc.abstractmethod
    def cleanup(self):
        """Cleanup resources used by the OCR engine."""
        pass