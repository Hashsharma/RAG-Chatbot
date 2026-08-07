import asyncio
from fastapi import APIRouter, HTTPException
from llama_index.core import VectorStoreIndex
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine

from app.schemas.model_schemas import QueryRequest, QueryResponse
from app.core.model_loader import get_model
from app.core.vector_store import get_vector_store
from app.core.config import get_settings
import asyncio
from app.core.vector_store import get_chroma_client, get_index_vector_store
from llama_index.core.retrievers import QueryFusionRetriever
from llama_index.llms.openai_like import OpenAILike
from llama_index.core import Settings
from llama_index.retrievers.bm25 import BM25Retriever
from app.core.bm25_retriever import get_bm25_retriever
from app.core.config import get_settings

router = APIRouter()
settings = get_settings()

llm = OpenAILike(
    model=settings.llm_model,
    api_base=settings.llm_api_base,
    api_key=settings.llm_api_key,
    is_chat_model=settings.llm_is_chat_model,
)
Settings.llm = llm

@router.get("/query", response_model=QueryResponse)
async def query():
    """
    Simple RAG query: embed -> search -> return results
    """
    try:
        # Get components (already loaded)
        embed_model = get_model()
        chroma_client = get_chroma_client()
        
        # Get collection
        settings = get_settings()
        collection = chroma_client.get_or_create_collection(
            name=settings.chroma_collection
        )
        
        # 1. Generate query embedding (offload to thread pool)
        loop = asyncio.get_event_loop()
        query_embedding = await loop.run_in_executor(
            None,
            lambda: embed_model.get_query_embedding("In what city and state did Beyonce grow up?")
        )
        
        # 2. Query ChromaDB
        query_results = collection.query(
            query_embeddings=[query_embedding],
            n_results=3,
            include=["documents", "metadatas", "distances"]  # Get everything
        )
        
        # 3. Format results
        sources = []
        if query_results['documents'] and len(query_results['documents'][0]) > 0:
            for i in range(len(query_results['documents'][0])):
                sources.append({
                    "text": query_results['documents'][0][i],
                    "score": 1 - query_results['distances'][0][i],  # Convert distance to similarity
                    "metadata": query_results['metadatas'][0][i] if query_results['metadatas'] else {}
                })
        
        if sources:
            # You can customize this: return top result, or combine all
            answer = sources[0]['text']  # Simple: just return the most relevant
            # Or combine all:
            # answer = "\n\n".join([s['text'] for s in sources])
        else:
            answer = "No relevant documents found."
        
        return QueryResponse(
            answer=answer,
            sources=sources
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/hybrid-query")
async def hybrid_query():
    try:
        query_text = "In what city and state did Beyonce grow up?"
        
        # Try BM25 first
        bm25_retriever = get_bm25_retriever()
        vector_retriever = get_index_vector_store().as_retriever(
            similarity_top_k=6
        )
        
        loop = asyncio.get_event_loop()
        
        if bm25_retriever:
            try:
                # Hybrid: BM25 + Vector
                fusion_retriever = QueryFusionRetriever(
                    [bm25_retriever, vector_retriever],
                    similarity_top_k=4,
                    num_queries=2,
                    mode="reciprocal_rerank",
                    # llm=Settings.llm
                )
                
                results = await loop.run_in_executor(
                    None,
                    lambda: fusion_retriever.retrieve(query_text)
                )
                mode = "BM25+Vector"
            except Exception as e:
                print(f"⚠️ BM25 failed, falling back to vector only: {e}")
                results = await loop.run_in_executor(
                    None,
                    lambda: vector_retriever.retrieve(query_text)
                )
                mode = "Vector only (BM25 failed)"
        else:
            # Vector only
            results = await loop.run_in_executor(
                None,
                lambda: vector_retriever.retrieve(query_text)
            )
            mode = "Vector only"
        
        # Format results
        sources = [{
            "text": r.node.text[:300],
            "score": r.score,
            "metadata": r.node.metadata.get("answer")
        } for r in results[:4]]
        
        return {
            "query": query_text,
            "answer": sources[0]['metadata'] if sources else "No results",
            # "sources": sources,
            "mode": mode
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/hybrid-query")
async def hybrid_query(request: QueryRequest):
    try:
        query_text = request.query

        # Try BM25 first
        bm25_retriever = get_bm25_retriever()

        vector_retriever = get_index_vector_store().as_retriever(
            similarity_top_k=6
        )

        loop = asyncio.get_event_loop()

        if bm25_retriever:
            try:
                # Hybrid: BM25 + Vector
                fusion_retriever = QueryFusionRetriever(
                    [bm25_retriever, vector_retriever],
                    similarity_top_k=4,
                    num_queries=2,
                    mode="reciprocal_rerank",
                )

                results = await loop.run_in_executor(
                    None,
                    lambda: fusion_retriever.retrieve(query_text)
                )

                mode = "BM25+Vector"

            except Exception as e:
                print(f"⚠️ BM25 failed, falling back to vector only: {e}")

                results = await loop.run_in_executor(
                    None,
                    lambda: vector_retriever.retrieve(query_text)
                )

                mode = "Vector only (BM25 failed)"

        else:
            # Vector only
            results = await loop.run_in_executor(
                None,
                lambda: vector_retriever.retrieve(query_text)
            )

            mode = "Vector only"


        # Format results
        sources = [
            {
                "text": r.node.text[:300],
                "score": r.score,
                "metadata": r.node.metadata.get("answer")
            }
            for r in results[:4]
        ]


        return {
            "query": query_text,
            "answer": sources[0]["metadata"] if sources else "No results",
            "sources": sources,
            "mode": mode
        }


    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.get("/query-user")
async def get_user():
    return {"user": "0001"}

@router.get("/stats")
async def get_stats():
    """Get collection statistics"""
    try:
        chroma_client = get_chroma_client()
        settings = get_settings()
        collection = chroma_client.get_or_create_collection(
            name=settings.chroma_collection
        )
        
        return {
            "total_documents": collection.count(),
            "collection_name": collection.name,
            "metadata": collection.metadata
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@router.get("/stats")
async def get_stats():
    """Get vector store statistics."""
    try:
        vector_store = get_vector_store()
        collection = vector_store._collection  # Access underlying Chroma collection
        
        return {
            "total_documents": collection.count(),
            "collection_name": collection.name,
            "metadata": collection.metadata
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/greetings")
async def greetings():
    return {"greetings": "Welcome to the RAG applications builder"}

