from __future__ import annotations

from typing import TYPE_CHECKING

from app.config import EMBEDDING_MODEL_NAME

if TYPE_CHECKING:
    from sentence_transformers import SentenceTransformer

_model: SentenceTransformer | None = None


def _get_model() -> "SentenceTransformer":
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    return _model


def encode(text: str) -> list[float]:
    model = _get_model()
    vec = model.encode(text, normalize_embeddings=True)
    return vec.tolist()


def encode_batch(texts: list[str], batch_size: int = 32) -> list[list[float]]:
    if not texts:
        return []
    model = _get_model()
    matrix = model.encode(texts, normalize_embeddings=True, batch_size=batch_size)
    return [row.tolist() for row in matrix]
