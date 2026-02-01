import os

QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))
QDRANT_URL = os.getenv("QDRANT_URL", f"http://{QDRANT_HOST}:{QDRANT_PORT}")

DATASET_PATH = os.getenv("DATASET_PATH", "data/dataset.json")

EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL", "deepvk/USER-bge-m3")
EMBEDDING_VECTOR_SIZE = 1024
