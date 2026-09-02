import pytesseract
from PIL import Image
from io import BytesIO


class ImageParser:
    """Extract text from images using OCR"""

    @staticmethod
    def extract_text(image_file) -> str:
        """
        OCR to extract text from medical images
        """
        try:
            image = Image.open(BytesIO(image_file.read()))

            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')

            # Perform OCR
            text = pytesseract.image_to_string(image)

            return text.strip()
        except Exception as e:
            raise Exception(f"Image OCR error: {str(e)}")