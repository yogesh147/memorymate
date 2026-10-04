from pathlib import Path

from sqlalchemy.orm import Session

from ..models import Memory
from .embeddings import create_embedding


def split_text(
        text: str,
        chunk_size: int = 700,
        overlap: int = 100,
):
    text = text.strip()

    if not text:
        return []

    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start = end - overlap

        if start < 0:
            start = 0

    return chunks


def ingest_text(
        db: Session,
        text: str,
        source: str,
        source_type: str = "text",
):
    chunks = split_text(text)

    memories = []

    for chunk in chunks:
        embedding = create_embedding(chunk)

        memory = Memory(
            content=chunk,
            source=source,
            source_type=source_type,
            embedding=embedding,
            confidence=1.0,
        )

        db.add(memory)
        memories.append(memory)

    db.commit()

    for memory in memories:
        db.refresh(memory)

    return memories


def ingest_file(
        db: Session,
        file_path: str,
):
    path = Path(file_path)

    if path.suffix.lower() not in [".txt", ".md"]:
        raise ValueError(
            "Currently only TXT and MD files are supported."
        )

    text = path.read_text(
        encoding="utf-8",
        errors="ignore",
    )

    return ingest_text(
        db=db,
        text=text,
        source=path.name,
        source_type="file",
    )
