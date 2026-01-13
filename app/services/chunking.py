import re
from typing import Dict, List

class SemanticChunker:
    @staticmethod
    def chunk_by_sentences(text: str, chunk_size: int, overlap: int) -> List[str]:
        chunk_size = int(chunk_size)
        overlap = int(overlap)
        
        #Split by punctuation into sentences
        text = re.sub(r"\s+", " ", text)
        sentences = re.split(r"(?<=[.!?])\s+", text)
        chunks = []
        current_chunk: List[str] = []
        current_size = 0 #current word count for chunk

        for sentence in sentences:
            words = sentence.split()
            sentence_size = len(words)

            #end curr chunk if size exceeded by sentence
            if current_size + sentence_size > chunk_size and current_chunk:
                chunks.append(" ".join(current_chunk))

                overlap_sentences: List[str] = []
                overlap_count = 0
                for s in reversed(current_chunk):
                    w = s.split()
                    if overlap_count + len(w) <= overlap:
                        overlap_sentences.insert(0, s)
                        overlap_count += len(w)
                    else:
                        break

                current_chunk = overlap_sentences
                current_size = overlap_count

            #Add sentence to curr chunk
            current_chunk.append(sentence)
            current_size += sentence_size

        #add final chunk
        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks

    @staticmethod
    def chunk_by_sections(text: str, chunk_size: int, overlap: int) -> List[Dict]:
        #Split into sections then use sentence splitting method
        #Returns dict of chunked text, section titles, and chunk idx

        #Attempt to identify headers/titles
        lines = text.split("\n")
        sections = []
        current_section = {"title": "Introduction", "content": ""}

        for line in lines:
            line = line.strip()
            #skip empties
            if not line:
                continue

            if (
                #check for headers/titles
                len(line) < 100
                and (line.isupper() or re.match(r"^\d+\.", line) or re.match(r"^[A-Z\s]{3,}$", line))
            ):
                if current_section["content"]:
                    sections.append(current_section) # save prev
                current_section = {"title": line, "content": ""} #new section 
            else:
                current_section["content"] += line + " "

        if current_section["content"]:
            sections.append(current_section)

        #sections into sentences
        all_chunks: List[Dict] = []
        for section in sections:
            section_chunks = SemanticChunker.chunk_by_sentences(
                section["content"], chunk_size, overlap
            )
            for i, chunk in enumerate(section_chunks):
                all_chunks.append({"text": chunk, "section": section["title"], "chunk_index": i})

        return all_chunks