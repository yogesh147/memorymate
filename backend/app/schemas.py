from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class MemoryCreate(BaseModel):
    content: str
    person: Optional[str] = None
    source: Optional[str] = None
    source_type: Optional[str] = "text"


class MemoryResponse(BaseModel):
    id: int
    content: str
    person: Optional[str]
    source: Optional[str]
    source_type: Optional[str]
    confidence: float
    created_at: datetime

    class Config:
        def __init__(self):
            pass

        from_attributes = True


class SearchRequest(BaseModel):
    question: str
    person: Optional[str] = None


class SearchResponse(BaseModel):
    answer: str
    memories: list[MemoryResponse]


class FriendCreate(BaseModel):
    name: str
