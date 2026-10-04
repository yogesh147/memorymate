import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    def __init__(self):
        pass

    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/memorymate",
    )

    OLLAMA_URL = os.getenv(
        "OLLAMA_URL",
        "http://localhost:11434",
    )

    GEMMA_MODEL = os.getenv(
        "GEMMA_MODEL",
        "gemma3:4b",
    )

    EMBEDDING_MODEL = os.getenv(
        "EMBEDDING_MODEL",
        "all-MiniLM-L6-v2",
    )


settings = Settings()
