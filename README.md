# LegalRAG

**LegalRAG** is a Retrieval-Augmented Generation (RAG) application designed to help users understand **End User License Agreements (EULAs)**, **Terms of Service (ToS)**, **Privacy Policies**, and other contracts through semantic search and grounded question answering.

The system ingests PDF legal documents, semantically chunks and embeds them, stores embeddings in a vector database, and uses a large language model to generate accurate, context-grounded answers derived strictly from the source documents.

---

## Key Capabilities

* PDF ingestion and processing
* Semantic chunking by legal sections
* Vector similarity search with ChromaDB
* Grounded LLM responses via AWS Bedrock (Claude)
* FastAPI REST API
* Interactive web UI
* Cloud-ready architecture (AWS + ChromaDB Cloud)

---

## Architecture Overview

LegalRAG follows a modular, service-oriented design to support collaborative development and clean separation of concerns.

### Document Ingestion

* PDFs uploaded via UI or API
* Text extraction and cleaning
* Metadata detection (EULA vs ToS)

### Semantic Indexing

* Section-aware chunking
* Sentence-level overlap handling
* Embeddings generated using Sentence Transformers
* Chunks persisted in ChromaDB Cloud

### Retrieval & Generation

* Query embedding
* Vector similarity search (top-K)
* Context assembly from retrieved chunks
* Answer generation using Claude via AWS Bedrock

### Presentation Layer

* REST API for programmatic access
* Web UI for document upload and querying

---

## Project Structure

```
Legal-Rag/
├─ app/
│  ├─ main.py                 # FastAPI app entry point
│  ├─ core/
│  │  ├─ config.py            # Environment-based configuration
│  │  └─ state.py             # Shared application state
│  ├─ api/
│  │  ├─ routes.py            # REST endpoints
│  │  └─ schemas.py           # Pydantic models
│  ├─ services/
│  │  ├─ bedrock_llm.py       # AWS Bedrock / Claude interface
│  │  ├─ s3_manager.py        # S3 storage abstraction
│  │  ├─ pdf_processor.py     # PDF parsing & metadata extraction
│  │  ├─ chunking.py          # Semantic chunking logic
│  │  ├─ embedding_manager.py # SentenceTransformer embeddings
│  │  ├─ chroma_manager.py    # ChromaDB Cloud integration
│  │  ├─ document_processor.py# End-to-end ingestion pipeline
│  │  └─ rag_system.py        # Retrieval + generation orchestration
│  └─ ui/
│  │  ├─ routes.py            # UI routes
│  │  ├─ static/
│  │  │  ├─ css/
│  │  │  │  └─ style.css
│  │  │  └─ js/
│  │  │     └─ main.js
│  │  └─ templates/
│  │     └─ index.html        # Web interface
├─ requirements.txt
├─ .env.example
└─ README.md
```

This structure enables multiple contributors to work independently on backend services, retrieval logic, API design, UI, and infrastructure.

---

## Technology Stack

* **Backend Framework:** FastAPI
* **LLM Provider:** AWS Bedrock (Claude models)
* **Vector Database:** ChromaDB Cloud
* **Embeddings:** Sentence Transformers (MiniLM)
* **Storage:** Amazon S3
* **Frontend:** HTML / CSS / Vanilla JavaScript
* **Language:** Python 3.10+

---

## Setup Instructions

### Install Dependencies

```
pip install -r requirements.txt
```

---

### Configure Environment Variables

Copy the example environment file:

```
cp .env.example .env
```

Populate the following values:

* AWS credentials with `bedrock:InvokeModel` permissions
* ChromaDB Cloud credentials
* Optional tuning parameters (chunk size, overlap, top-K)

---

### Enable AWS Bedrock

* Request access to Anthropic Claude models in the AWS Bedrock console
* Ensure your IAM role or user has permission to invoke the model

---

### Run the Application

```
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

### Access the UI

Open your browser at:

```
http://localhost:8000
```

---

## API Endpoints

| Method | Endpoint             | Description              |
| ------ | -------------------- | ------------------------ |
| GET    | `/`                  | Web UI                   |
| POST   | `/upload`            | Upload and process a PDF |
| POST   | `/query`             | Query the RAG system     |
| GET    | `/documents`         | List indexed documents   |
| GET    | `/document/{doc_id}` | Document details         |
| DELETE | `/document/{doc_id}` | Delete a document        |
| GET    | `/health`            | Health check             |

---

## Example Use Cases

* Understanding data retention clauses
* Identifying arbitration or liability limitations
* Comparing ToS obligations across platforms
* Rapid legal document triage and review

---

## Development Notes

* Stateless retrieval: all semantic knowledge resides in the vector store
* Grounded generation: answers are derived strictly from retrieved document chunks
* Cloud persistence: ChromaDB Cloud and S3 persist data across restarts
* Extensible design: easy to add metadata filters, distance thresholds, or document routing logic

---

## Security Considerations

* Do not commit `.env` files
* Prefer IAM roles over static AWS credentials
* Treat uploaded legal documents as sensitive data

---

## Roadmap Ideas

* Multi-tenant document isolation
* Citation highlighting in the UI
* Role-based access control
* Hybrid keyword + vector retrieval

---

## License

This project is provided for educational and internal tooling purposes.
Review security, compliance, and licensing requirements before deploying to production environments.

---

**LegalRAG** — making complex legal documents understandable through grounded AI.
