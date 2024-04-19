from datetime import datetime
import os

def generate_file_name():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # Format: YYYYMMDD_HHMMSS
    return f"file_{timestamp}.pdf"

def is_pdf(filename: str) -> bool:
    """Check if the filename has a PDF extension"""
    _, extension = os.path.splitext(filename)
    return extension.lower() == ".pdf"
