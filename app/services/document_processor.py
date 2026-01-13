import hashlib
from app.core.config import Config
from app.services.pdf_processor import PDFProcessor
from app.services.chunking import SemanticChunker
from app.services.embedding_manager import EmbeddingManager
from app.services.chroma_manager import ChromaDBManager


class DocumentProcessor:
    def __init__(self):
        # TODO: Add S3 upload for raw PDFs
        # self.s3_manager = S3Manager()

        self.pdf_processor = PDFProcessor()
        self.chunker = SemanticChunker()
        self.embedding_manager = EmbeddingManager()
        self.chroma_manager = ChromaDBManager()

        # TODO: Pass config in via constructor instead of using Config directly

    def process_document(self, pdf_bytes: bytes, filename: str):
        text = self.pdf_processor.extract_text(pdf_bytes)
        clean_text = self.pdf_processor.clean_text(text)

        # TODO: Add document-level metadata extraction
        # metadata = self.pdf_processor.extract_metadata(clean_text, filename)

        # TODO: Handle PDFs with no extractable text (OCR)
        if not clean_text.strip():
            raise ValueError(f"No extractable text found in '{filename}'")

        chunks = self.chunker.chunk_by_sections(
            clean_text, Config.CHUNK_SIZE, Config.CHUNK_OVERLAP
        )

        chunk_texts = [chunk["text"] for chunk in chunks]

        # TODO: Add batching / retry logic for embeddings
        embeddings = self.embedding_manager.embed_texts(chunk_texts)

        # TODO: Replace filename-based ID with content-based ID
        doc_id = hashlib.md5(filename.encode()).hexdigest()

        # TODO: Store document metadata with chunks
        self.chroma_manager.add_chunks(chunks, doc_id, embeddings)

        # TODO: Upload raw PDFs to object storage
        # self.s3_manager.upload_file(
        #     Config.RAW_BUCKET, filename, pdf_bytes, "application/pdf"
        # )

        return {
            "doc_id": doc_id,
            "filename": filename,
            "chunk_count": len(chunks),
            # TODO: Return metadata once implemented
            # "metadata": metadata,
        }
