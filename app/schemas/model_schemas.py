from pydantic import BaseModel
from typing import List, Dict, Optional

class QueryRequest(BaseModel):
    query: str
    top_k: int = 5

class SourceNode(BaseModel):
    text: str
    score: float
    metadata: Optional[Dict] = None

class QueryResponse(BaseModel):
    answer: str
    sources: List[SourceNode] = []