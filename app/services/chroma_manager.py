from typing import Dict, List
import chromadb
from app.core.config import Config

class ChromaDBManager:
    def __init__(self):
        self.client = chromadb.CloudClient(
            tenant=Config.CHROMA_TENANT,
            database=Config.CHROMA_DATABASE,
            api_key=Config.CHROMA_API_KEY,
        )
        self._initialize_collection()

    def _initialize_collection(self):
        try:
            self.collection = self.client.get_collection(Config.COLLECTION_NAME)
        except Exception:
            self.collection = self.client.create_collection(
                name=Config.COLLECTION_NAME,
                metadata={"description": "EULA and ToS document embeddings"},
            )

    def add_chunks(self, chunks: List[Dict], doc_id: str, embeddings: List[List[float]]):
        ids = [f"{doc_id}_chunk_{i}" for i in range(len(chunks))]
        documents = [chunk["text"] for chunk in chunks]
        metadatas = [
            {
                "doc_id": doc_id,
                "section": chunk.get("section", "unknown"),
                "chunk_index": chunk.get("chunk_index", i),
            }
            for i, chunk in enumerate(chunks)
        ]

        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )

    def query(self, query_embedding: List[float], n_results: int = 5) -> Dict:
        results = self.collection.query(query_embeddings=[query_embedding], n_results=n_results)

        # Filter out any chunks with negative relevance (distance < 0)
        if "distances" in results and results["distances"]:
            filtered_ids, filtered_docs, filtered_meta, filtered_dist = [], [], [], []
            for i, dist in enumerate(results["distances"][0]):
                if dist < 1:  # keep only non-negative relevance
                    filtered_ids.append(results["ids"][0][i])
                    filtered_docs.append(results["documents"][0][i])
                    filtered_meta.append(results["metadatas"][0][i])
                    filtered_dist.append(dist)
            results["ids"][0] = filtered_ids
            results["documents"][0] = filtered_docs
            results["metadatas"][0] = filtered_meta
            results["distances"][0] = filtered_dist

        return results

    def delete_by_doc_id(self, doc_id: str):
        try:
            results = self.collection.get(where={"doc_id": doc_id})
            if results and "ids" in results and results["ids"]:
                self.collection.delete(ids=results["ids"])
        except Exception as e:
            print(f"Error deleting doc_id {doc_id}: {e}")
