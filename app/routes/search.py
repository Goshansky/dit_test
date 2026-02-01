from litestar import post, Request
from pydantic import BaseModel

from app.vector_store import search as vector_search


class SearchBody(BaseModel):
    query: str


@post("/search", sync_to_thread=True)
def search_endpoint(request: Request, data: SearchBody) -> dict:
    client = request.app.state.qdrant
    results = vector_search(client, data.query, top_k=5)
    return {"query": data.query, "results": results}
