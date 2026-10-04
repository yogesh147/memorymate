from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from .routes import friends, memories, search

app = FastAPI(
    title="MemoryMate API",
    description="AI memory assistant built for a friend.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    Base.metadata.create_all(
        bind=engine
    )

@app.get("/")
def root():
    return {
        "name": "MemoryMate",
        "status": "running",
    }

@app.get("/health")
def health():
    return {
        "status": "healthy",
    }


app.include_router(
    memories.router
)

app.include_router(
    search.router
)

app.include_router(
    friends.router
)
