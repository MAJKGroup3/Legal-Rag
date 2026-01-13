import re
from datetime import datetime
from io import BytesIO
from typing import Dict
import PyPDF2


class PDFProcessor:
    @staticmethod
    def extract_text(pdf_bytes: bytes) -> str:
        pdf_file = BytesIO(pdf_bytes)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += (page.extract_text() or "") + "\n"
        return text

    @staticmethod
    def clean_text(text):
        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"[^\w\s.,;:!?()\-\'\"]+", "", text)
        return text.strip()
    
    @staticmethod
    def extract_metadata(text, filename):
        metadata = {
            "filename": filename,
            "doc_type": "unknown",
            "timestamp": datetime.now().isoformat(),
            "word_count": len(text.split()),
            "char_count": len(text)
        }

        return metadata