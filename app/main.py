from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import get_settings
from app.core.model_loader import load_model
from app.services.rag_service import router as rag_router
from app.core.vector_store import load_vector_store

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: load the model
    settings = get_settings()
    load_model(settings.model_name)

    # Load vector store
    load_vector_store(settings.chroma_db_path, settings.chroma_collection)
    # load_bm25_retriever()  # Load BM25
    print(f"✅ Model '{settings.model_name}' loaded successfully.")
    yield
    # Shutdown: any cleanup (if needed)
    # For this simple app, we don't need to unload the model.

app = FastAPI(title="RAG API", lifespan=lifespan)
app.include_router(rag_router, prefix="/api/v1")