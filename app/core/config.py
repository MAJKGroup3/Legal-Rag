import os

class Config:
    
    # AWS KEYS
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_REGION = os.getenv("AWS_REGION")


    # BEDROCK SETUP

    BEDROCK_MODEL_ID = os.getenv("BEDROCK_MODEL_ID",
    "anthropic.claude-3-sonnet-20240229-v1:0")  
    PROCESSED_BUCKET = os.getenv("PROCESSED_BUCKET", "processed-eula-docs")

    # Chroma cloud

    CHROMA_API_KEY = os.getenv("CHROMA_API_KEY", "")
    CHROMA_TENANT = os.getenv("CHROMA_TENANT", "")
    CHROMA_DATABASE = os.getenv("CHROMA_DATABASE", "eula-docs")
    CHROMA_COLLECTION = os.getenv("CHROMA_COLLECTION", "eula-docs")

    # Processing

    CHUNK_SIZE = os.getenv("CHUNK_SIZE", 1000)
    CHUNK_OVERLAP = os.getenv("CHUNK_OVERLAP", 200)

    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

    TOP_K_CHUNKS = int(os.getenv("TOP_K_CHUNKS", "5"))

    # Local
    UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./uploads")

