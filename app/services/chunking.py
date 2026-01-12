import re
from typing import List, Dict


class SemanticChunker:
    def chunk_by_sentences(self, text: str, chunk_size: int) -> List[str]:
        sentences = re.split(r"(?<=[.!?])\s+", text)
        chunks = []
        current_chunk = []
        current_size = 0

        for sentence in sentences:
            words = sentence.split()
            if current_size + len(words) > chunk_size and current_chunk:
                chunks.append(" ".join(current_chunk))
                current_chunk = []
                current_size = 0

            current_chunk.append(sentence)
            current_size += len(words)

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks

    def chunk_by_sections(self, text: str, chunk_size: int) -> List[Dict]:
        sections = text.split("\n\n")
        all_chunks = []

        for sec_idx, section in enumerate(sections):
            section_text = section.strip()
            if not section_text:
                continue

            sentence_chunks = self.chunk_by_sentences(section_text, chunk_size)
            for i, chunk in enumerate(sentence_chunks):
                all_chunks.append({
                    "text": chunk,
                    "section": f"Section {sec_idx+1}",
                    "chunk_index": i
                })

        return all_chunks


if __name__ == "__main__":
    test_paragraph = (
        """Welcome to our service. By using this platform, you agree to comply with our terms and conditions. 
        Your privacy is important to us, and we take measures to protect your personal data. 
        We may collect information about your usage patterns to improve our services. 
        Please note that unauthorized access or misuse of the platform is strictly prohibited. 
        Our liability is limited to the extent permitted by law. 
        Users are responsible for maintaining the confidentiality of their accounts. 
        Content uploaded to our platform must not violate copyright or intellectual property rights. 
        We reserve the right to terminate accounts that breach these rules. 
        By continuing to use the platform, you consent to receive communications related to service updates. 
        These terms may be updated periodically, and continued use constitutes acceptance of the changes. 
        For further information, please contact our support team."""
    )

    chunker = SemanticChunker()
    chunks = chunker.chunk_by_sentences(test_paragraph, chunk_size=20)
    print("Sentence-based chunks:")
    for idx, c in enumerate(chunks):
        print(f"Chunk {idx+1}: {c}\n")

    section_chunks = chunker.chunk_by_sections(test_paragraph, chunk_size=20)
    print("Section-based chunks:")
    for c in section_chunks:
        print(c)
