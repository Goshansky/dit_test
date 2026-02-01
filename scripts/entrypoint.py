"""
Entrypoint для контейнера: ждёт Qdrant, при пустой коллекции запускает индексацию, затем uvicorn.
"""
import os
import subprocess
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.config import COLLECTION_NAME
from app.main import get_qdrant


def wait_for_qdrant(max_attempts: int = 60, interval: float = 1.0) -> None:
    for _ in range(max_attempts):
        try:
            client = get_qdrant()
            client.get_collections()
            client.close()
            return
        except Exception:
            time.sleep(interval)
    print("Qdrant недоступен, выход.")
    sys.exit(1)


def need_indexing() -> bool:
    try:
        client = get_qdrant()
        try:
            info = client.get_collection(COLLECTION_NAME)
            return info.points_count == 0
        except Exception:
            return True
        finally:
            client.close()
    except Exception:
        return True


def main() -> None:
    wait_for_qdrant()

    if need_indexing():
        subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "scripts" / "index_data.py")],
            check=True,
            cwd=str(PROJECT_ROOT),
        )

    os.execv(sys.executable, [
        sys.executable, "-m", "uvicorn", "app.main:app",
        "--host", "0.0.0.0", "--port", "8000",
    ])


if __name__ == "__main__":
    main()
