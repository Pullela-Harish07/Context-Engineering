import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Centralized configuration management"""

    # API Keys
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

    # Email Configuration
    SMTP_EMAIL = os.getenv("SMTP_EMAIL")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
    SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))

    # Model Configuration
    MODEL_NAME = "gemini-2.5-flash"
    TEMPERATURE = 0.1  # Lower for medical accuracy

    # Application Settings
    MAX_FILE_SIZE_MB = 10
    SUPPORTED_IMAGE_FORMATS = [".jpg", ".jpeg", ".png"]
    SUPPORTED_PDF_FORMATS = [".pdf"]

    @classmethod
    def validate(cls):
        """Validate required settings"""
        if not cls.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY not found in .env file")
        return True


settings = Settings()
settings.validate()