# core/bm25_retriever.py

import pickle
import random
from pathlib import Path
from llama_index.retrievers.bm25 import BM25Retriever
from llama_index.core import Document
from llama_index.core.node_parser import SimpleNodeParser
from app.core.vector_store import get_chroma_client
from app.core.config import get_settings

_bm25_retriever = None
CACHE_DIR = Path("./cache")
CACHE_DIR.mkdir(exist_ok=True)

from pathlib import Path

def get_bm25_retriever(force_reload: bool = False):
    """Load BM25 retriever from persistent storage"""
    global _bm25_retriever
    
    if _bm25_retriever is not None and not force_reload:
        return _bm25_retriever
    
    print("🔄 Loading BM25 retriever from persistent storage...")

    try:
        # bm25_retriever.py -> core -> app -> project
        project_root = Path(__file__).resolve().parents[2]

        bm25_path = project_root / "storage" / "bm25_db" / "bm25_persists"

        print(f"📂 BM25 path: {bm25_path}")

        _bm25_retriever = BM25Retriever.from_persist_dir(
            str(bm25_path)
        )

        _bm25_retriever.similarity_top_k = 4

        print("✅ BM25 loaded successfully")
        return _bm25_retriever

    except Exception as e:
        print(f"❌ Error loading BM25: {e}")
        return None

    
def clear_bm25_cache():
    """Clear the BM25 cache"""
    cache_file = CACHE_DIR / "bm25_index_sample.pkl"
    if cache_file.exists():
        cache_file.unlink()
        print("✅ BM25 cache cleared")
        return True
    return False