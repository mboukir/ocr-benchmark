from .base import BaseOCR
from .paddleocr import PaddleOCR
from .mmocr import MMOCR
from .tesseract import TesseractOCR
from .easyocr import EasyOCR

__all__ = [
    'BaseOCR',
    'PaddleOCR',
    'MMOCR',
    'TesseractOCR',
    'EasyOCR'
]