from datetime import datetime

from pgvector.sqlalchemy import Vector
from sqlalchemy import (
    Column,
    DateTime,
    Float,
    Integer,
    String,
    Text,
)

from .database import Base


class Memory(Base):
    __tablename__ = "memories"

    id = Column(Integer, primary_key=True, index=True)

    content = Column(Text, nullable=False)

    person = Column(String(255), nullable=True)

    source = Column(String(500), nullable=True)

    source_type = Column(String(50), nullable=True)

    metadata_json = Column(Text, nullable=True)

    confidence = Column(Float, default=1.0)

    embedding = Column(Vector(384), nullable=True)

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )


class Friend(Base):
    __tablename__ = "friends"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(255), unique=True, nullable=False)

    interests = Column(Text, nullable=True)

    projects = Column(Text, nullable=True)

    preferences = Column(Text, nullable=True)

    notes = Column(Text, nullable=True)

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
