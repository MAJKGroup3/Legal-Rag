import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import Config
from app.core.state import AppState
from app.services.s3_manager import S3Manager
from app.services.rag_system import RAGSystem
from app.services.document_processor import DocumentProcessor
from app.api.routes import router as api_router
from app.ui.routes import router as ui_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="EULA/ToS RAG System",
        description="Semantic search and question answering for EULA and Terms of Service documents",
        version="1.0.0",
    )

    # Mount static files (CSS, JS) for frontend
    app.mount("/static", StaticFiles(directory="app/ui/static"), name="static")

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Ensure upload dir exists
    os.makedirs(Config.UPLOAD_DIR, exist_ok=True)

    # State container
    app.state.app_state = AppState()

    # Router inits
    app.include_router(ui_router)
    app.include_router(api_router)

    @app.on_event("startup")
    async def startup_event():
        print("Initializing RAG system...")

        # Make buckets
        s3 = S3Manager()
        s3.create_buckets()

        # Init RAG and doc processor
        app.state.app_state.rag_system = RAGSystem()
        app.state.app_state.doc_processor = DocumentProcessor()

        print("RAG system initialized successfully!")

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
