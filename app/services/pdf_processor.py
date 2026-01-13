import re
from datetime import datetime
from io import BytesIO
import PyPDF2


class PDFProcessor:
    @staticmethod
    def extract_text(pdf_bytes):
        if not pdf_bytes:
            raise ValueError("pdf_bytes is empty")

        try:
            pdf_file = BytesIO(pdf_bytes)
            pdf_reader = PyPDF2.PdfReader(pdf_file)

            # Common issue: encrypted PDFs
            if getattr(pdf_reader, "is_encrypted", False):
                # Try empty password first; if it fails, treat as unsupported
                try:
                    pdf_reader.decrypt("")
                except Exception as e:
                    raise ValueError("PDF is encrypted and cannot be processed") from e

            text_parts = []
            for i, page in enumerate(pdf_reader.pages):
                try:
                    text_parts.append((page.extract_text() or "") + "\n")
                except Exception as e:
                    raise ValueError(f"Failed extracting text from page {i}") from e

            return "".join(text_parts)

        except Exception as e:
            raise ValueError(f"Failed to read PDF: {e}") from e

    @staticmethod
    def clean_text(text):
        if text is None:
            raise ValueError("text is None")
        if not isinstance(text, str):
            raise TypeError("text must be a string")

        try:
            text = text.replace("\r\n", "\n").replace("\r", "\n")

            # collapse spaces and tabs ONLY (preserve newlines)
            text = re.sub(r"[ \t]+", " ", text)

            # limit excessive blank lines
            text = re.sub(r"\n{3,}", "\n\n", text)

            # keep punctuation + newlines
            text = re.sub(r"[^\w\s.,;:!?()\-\'\"\n]+", "", text)
            return text.strip()
        except Exception as e:
            raise ValueError("Failed cleaning text") from e

    @staticmethod
    def extract_metadata(text, filename):
        if text is None:
            raise ValueError("text is None")
        if not isinstance(text, str):
            raise TypeError("text must be a string")

        if filename is None:
            raise ValueError("filename is None")
        if not isinstance(filename, str):
            raise TypeError("filename must be a string")

        metadata = {
            "filename": filename,
            "doc_type": "unknown",
            "timestamp": datetime.now().isoformat(),
            "word_count": len(text.split()),
            "char_count": len(text),
        }

        try:
            text_lower = text.lower()

            if ("end user license agreement" in text_lower) or ("eula" in text_lower):
                metadata["doc_type"] = "EULA"
            elif ("terms of service" in text_lower) or ("tos" in text_lower) or ("terms and conditions" in text_lower):
                metadata["doc_type"] = "ToS"
            elif "privacy policy" in text_lower:
                metadata["doc_type"] = "Privacy Policy"
            else:
                metadata["doc_type"] = "Other"

            return metadata

        except Exception as e:
            raise ValueError(f"Failed extracting metadata for '{filename}'") from e
