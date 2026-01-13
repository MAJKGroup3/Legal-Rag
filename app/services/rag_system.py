from typing import Dict
from app.core.config import Config
from app.services.bedrockllm import BedrockLLM
from app.services.embedding_manager import EmbeddingManager
from app.services.chroma_manager import ChromaDBManager

class RAGSystem:
    def __init__(self):
        self.embedding_manager = EmbeddingManager()
        self.chroma_manager = ChromaDBManager()
        self.bedrock_llm = BedrockLLM()

    def query(self, query, top_k: int = Config.TOP_K_CHUNKS) -> Dict:
        query_embedding = self.embedding_manager.embed_texts(query)
        results = self.chroma_manager.query(query_embedding, n_results=top_k)

        retrieved_chunks = []
        for i in range(len(results["ids"][0])):
            retrieved_chunks.append(
                {
                    "id": results["ids"][0][i],
                    "text": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i],
                    "distance": results.get("distances")[0][i]
                    if "distances" in results
                    else None,
                }
            )

        context = "\n\n".join(
            f"[Section: {chunk['metadata'].get('section', 'unknown')}]\n{chunk['text']}"
            for chunk in retrieved_chunks
        )

        answer = self.bedrock_llm.generate_response(query, context)

        return {
            "query": query,
            "answer": answer,
            "retrieved_chunks": retrieved_chunks,
            "num_chunks": len(retrieved_chunks),
        }
