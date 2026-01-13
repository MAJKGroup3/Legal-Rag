from typing import List
from sentence_transformers import SentenceTransformer
from app.core.config import Config


class EmbeddingManager:
    def __init__(self):
        self.model = SentenceTransformer(Config.EMBEDDING_MODEL)

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        embeddings = self.model.encode(texts, show_progress_bar=False)
        return embeddings.tolist()

    def embed_text(self, text: str) -> List[float]:
        embedding = self.model.encode([text], show_progress_bar=False)
        return embedding[0].tolist()
