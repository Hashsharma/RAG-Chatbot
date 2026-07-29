import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from pathlib import Path
from llama_index.core import VectorStoreIndex

_chroma_client = None
_vector_store = None
_storage_context = None
_vector_store_index = None

def load_vector_store(persist_path: str, collection_name: str = "qna_collections"):
    """
    Load ChromaDB vector store once on startup.
    """
    global _chroma_client, _vector_store, _storage_context, _vector_store_index
    
    if _vector_store is None:
        # Ensure the path exists
        Path(persist_path).mkdir(parents=True, exist_ok=True)
        
        # Initialize Chroma client
        _chroma_client = chromadb.PersistentClient(path=persist_path)
        
        # Get or create collection
        collection = _chroma_client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}  # Optional: set similarity metric
        )
        
        # Create vector store
        _vector_store = ChromaVectorStore(chroma_collection=collection)
        _vector_store_index = VectorStoreIndex.from_vector_store(_vector_store)
        # Create storage context
        _storage_context = StorageContext.from_defaults(vector_store=_vector_store)
        
        print(f"✅ Vector store loaded from: {persist_path}")
        print(f"   Collection: {collection_name}")
        print(f"   Total documents: {collection.count()}")
    
    return _vector_store, _storage_context

def get_vector_store():
    """Return the vector store instance."""
    if _vector_store is None:
        raise RuntimeError("Vector store not loaded. Call load_vector_store() on startup.")
    return _vector_store

def get_index_vector_store():
    """Return the vector store instance."""
    if _vector_store_index is None:
        raise RuntimeError("Vector store not loaded. Call load_vector_store() on startup.")
    return _vector_store_index


def get_storage_context():
    """Return the storage context instance."""
    if _storage_context is None:
        raise RuntimeError("Storage context not loaded. Call load_vector_store() on startup.")
    return _storage_context

def get_chroma_client():
    """Return the Chroma client instance (if needed for direct operations)."""
    if _chroma_client is None:
        raise RuntimeError("Chroma client not loaded. Call load_vector_store() on startup.")
    return _chroma_client