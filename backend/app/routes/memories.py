from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Memory
from ..schemas import MemoryCreate, MemoryResponse
from ..services.embeddings import create_embedding
from ..services.ingestion import ingest_text

router = APIRouter(
    prefix="/api/memories",
    tags=["memories"],
)


@router.post(
    "",
    response_model=MemoryResponse,
)
def create_memory(
        memory: MemoryCreate,
        db: Session = Depends(get_db),
):
    embedding = create_embedding(memory.content)

    item = Memory(
        content=memory.content,
        person=memory.person,
        source=memory.source,
        source_type=memory.source_type,
        embedding=embedding,
    )

    db.add(item)
    db.commit()
    db.refresh(item)

    return item


@router.get(
    "",
    response_model=list[MemoryResponse],
)
def get_memories(
        db: Session = Depends(get_db),
):
    return (
        db.query(Memory)
        .order_by(Memory.created_at.desc())
        .limit(100)
        .all()
    )


@router.delete("/{memory_id}")
def delete_memory(
        memory_id: int,
        db: Session = Depends(get_db),
):
    memory = (
        db.query(Memory)
        .filter(Memory.id == memory_id)
        .first()
    )

    if not memory:
        raise HTTPException(
            status_code=404,
            detail="Memory not found",
        )

    db.delete(memory)
    db.commit()

    return {"success": True}


@router.post("/upload")
async def upload_memory_file(
        file: UploadFile = File(...),
        db: Session = Depends(get_db),
):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Missing filename",
        )

    content = await file.read()

    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=400,
            detail="Only UTF-8 text files are supported in the MVP.",
        )

    memories = ingest_text(
        db=db,
        text=text,
        source=file.filename,
        source_type="file",
    )

    return {
        "success": True,
        "filename": file.filename,
        "memories_created": len(memories),
    }
