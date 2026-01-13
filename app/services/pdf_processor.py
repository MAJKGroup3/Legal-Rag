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

        text_lower = text.lower()
        if ("end user license agreement" in text_lower) or ("eula" in text_lower):
            metadata["doc_type"] = "EULA"
        elif ("terms of service" in text_lower) or ("tos" in text_lower) or ("terms and conditions" in text_lower):
            metadata["doc_type"] = "ToS"
        elif ("privacy policy" in text_lower):
            metadata["doc_type"] = "Privacy Policy"
        else:
            metadata["doc_type"] = "Other"

        return metadata