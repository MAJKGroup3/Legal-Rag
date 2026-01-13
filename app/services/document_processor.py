import hashlib
from app.core.config import Config
from app.services.s3_manager import S3Manager
from app.services.pdf_processor import PDFProcessor
from app.services.chunking import SemanticChunker
from app.services.embedding_manager import EmbeddingManager
from app.services.chroma_manager import ChromaDBManager

class DocumentProcessor:
    def __init__(self):
        self.s3_manager = S3Manager()
        self.pdf_processor = PDFProcessor()
        self.chunker = SemanticChunker()
        self.embedding_manager = EmbeddingManager()
        self.chroma_manager = ChromaDBManager()

    def process_document(self, pdf_bytes, filename):
        text = self.pdf_processor.extract_text(pdf_bytes)
        clean_text = self.pdf_processor.clean_text(text)
        metadata = self.pdf_processor.extract_metadata(clean_text, filename)

        chunks = self.chunker.chunk_by_sections(
            clean_text, Config.CHUNK_SIZE, Config.CHUNK_OVERLAP
        )

        chunk_texts = [chunk["text"] for chunk in chunks]
        embeddings = self.embedding_manager.embed_texts(chunk_texts)

        doc_id = hashlib.md5(filename.encode()).hexdigest()
        self.chroma_manager.add_chunks(chunks, doc_id, embeddings)

        self.s3_manager.upload_file(
            Config.RAW_BUCKET, filename, pdf_bytes, "application/pdf"
        )

        return {
            "doc_id": doc_id,
            "filename": filename,
            "metadata": metadata,
            "chunk_count": len(chunks)
        }
