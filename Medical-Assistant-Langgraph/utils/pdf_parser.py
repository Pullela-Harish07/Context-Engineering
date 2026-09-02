import PyPDF2
from io import BytesIO


class PDFParser:
    """Extract text from PDF medical reports"""

    @staticmethod
    def extract_text(pdf_file) -> str:
        """
        Extract text from uploaded PDF
        """
        try:
            pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_file.read()))
            text = ""

            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"

            return text.strip()
        except Exception as e:
            raise Exception(f"PDF parsing error: {str(e)}")