import requests

from ..config import settings


def ask_gemma(prompt: str) -> str:
    url = f"{settings.OLLAMA_URL}/api/generate"

    payload = {
        "model": settings.GEMMA_MODEL,
        "prompt": prompt,
        "stream": False,
    }

    response = requests.post(
        url,
        json=payload,
        timeout=120,
    )

    response.raise_for_status()

    data = response.json()

    return data.get("response", "").strip()
