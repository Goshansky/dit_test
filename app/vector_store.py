from __future__ import annotations

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from app.config import COLLECTION_NAME, EMBEDDING_VECTOR_SIZE
from app.embeddings import encode, encode_batch


def ensure_collection(client: QdrantClient) -> None:
    try:
        client.get_collection(COLLECTION_NAME)
    except Exception:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=EMBEDDING_VECTOR_SIZE,
                distance=Distance.COSINE,
            ),
        )


def upsert(client: QdrantClient, records: list[dict]) -> None:
    if not records:
        return
    ensure_collection(client)
    texts = [r["text"] for r in records]
    vectors = encode_batch(texts)
    points = [
        PointStruct(
            id=idx,
            vector=vec,
            payload={"id": r["id"], "text": r["text"]},
        )
        for idx, (r, vec) in enumerate(zip(records, vectors))
    ]
    client.upsert(collection_name=COLLECTION_NAME, points=points)


def search(client: QdrantClient, query: str, top_k: int = 5) -> list[dict]:
    query_vector = encode(query)
    response = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=top_k,
        with_payload=True,
    )
    points = response.points if hasattr(response, "points") else response.result.points
    return [
        {
            "id": str(hit.payload["id"]),
            "score": round(hit.score, 4),
            "text": hit.payload["text"],
        }
        for hit in points
    ]
