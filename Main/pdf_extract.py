"""
MODULE: pdf_extract.py
PURPOSE: Extracts raw text from PDF files.
TECHNIQUES:
- 'pypdf': Library to parse PDF internal structure.
- Text Processing: Iterates through pages and concatenates text.
- Error Handling: Returns None if text is unreadable (e.g., scanned images), signaling standard handling.
"""
from pypdf import PdfReader
from pathlib import Path
from typing import Optional

def extract_text(file_path: Path) -> Optional[str]:
    """
    Extracts text from a PDF file.
    Returns the extracted text, or None if no text could be extracted.
    """
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
        
        text = text.strip()
        if not text:
            return None
        
        return text
    except Exception as e:
        print(f"Error extracting text from {file_path.name}: {e}")
        return None
