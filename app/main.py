from contextlib import asynccontextmanager

from litestar import Litestar
from qdrant_client import QdrantClient

from app.config import QDRANT_HOST, QDRANT_PORT
from app.routes.search import search_endpoint


def get_qdrant() -> QdrantClient:
    return QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)


@asynccontextmanager
async def qdrant_lifespan(app: Litestar):
    client = get_qdrant()
    client.get_collections()
    setattr(app.state, "qdrant", client)
    try:
        yield
    finally:
        client.close()


app = Litestar(
    route_handlers=[search_endpoint],
    lifespan=[qdrant_lifespan],
)
