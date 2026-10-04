from functools import lru_cache

from sentence_transformers import SentenceTransformer

from ..config import settings


@lru_cache(maxsize=1)
def get_model():
    return SentenceTransformer(settings.EMBEDDING_MODEL)


def create_embedding(text: str) -> list[float]:
    model = get_model()

    embedding = model.encode(
        text,
        normalize_embeddings=True,
    )

    return embedding.tolist()
