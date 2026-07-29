import os
from functools import lru_cache
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings

_model = None   # Will hold the loaded model

def load_model(model_path: str, device: str = "cuda"):
    """
    Load the HuggingFace embedding model. Called once during app startup.
    """
    global _model
    if _model is None:
        # Initialize the embedding model
        _model = HuggingFaceEmbedding(
            model_name=model_path,
            device=device
        )
        # Set as the global embed model for LlamaIndex
        Settings.embed_model = _model

        # Optional: warm‑up to allocate memory / load tensors
        _model.get_text_embedding("warmup")
    return _model

def get_model():
    """Return the already loaded model instance."""
    if _model is None:
        raise RuntimeError("Model not loaded. Did you call load_model() on startup?")
    return _model