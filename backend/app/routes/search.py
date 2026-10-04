from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Memory
from ..schemas import SearchRequest, SearchResponse
from ..services.embeddings import create_embedding
from ..services.gemma import ask_gemma

router = APIRouter(
    prefix="/api/search",
    tags=["search"],
)


@router.post(
    "",
    response_model=SearchResponse,
)
def search_memories(
        request: SearchRequest,
        db: Session = Depends(get_db),
):
    query_embedding = create_embedding(
        request.question
    )

    distance = Memory.embedding.cosine_distance(
        query_embedding
    )

    query = (
        select(Memory)
        .order_by(distance)
        .limit(8)
    )

    if request.person:
        query = query.where(
            Memory.person.ilike(
                f"%{request.person}%"
            )
        )

    memories = db.execute(query).scalars().all()

    if not memories:
        return SearchResponse(
            answer="I couldn't find a relevant memory.",
            memories=[],
        )

    context = "\n\n".join(
        [
            f"Memory {i + 1}:\n{memory.content}\n"
            f"Source: {memory.source or 'Unknown'}"
            for i, memory in enumerate(memories)
        ]
    )

    prompt = f"""
You are MemoryMate, a private personal memory assistant.

Answer the user's question using ONLY the memories below.

If the memories do not contain enough information,
say that clearly.

Do not invent facts.

Question:
{request.question}

Memories:
{context}

Give a concise, friendly answer.
Mention useful sources when appropriate.
"""

    answer = ask_gemma(prompt)

    return SearchResponse(
        answer=answer,
        memories=memories,
    )
