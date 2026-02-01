import json
import sys
from pathlib import Path
from app.config import COLLECTION_NAME, DATASET_PATH
from app.main import get_qdrant
from app.vector_store import upsert

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def main() -> None:
    path = PROJECT_ROOT / DATASET_PATH if not Path(DATASET_PATH).is_absolute() else Path(DATASET_PATH)
    if not path.exists():
        print(f"Файл не найден: {path}")
        sys.exit(1)

    with open(path, encoding="utf-8") as f:
        records = json.load(f)

    if not records or not isinstance(records, list):
        print("Ожидается JSON-массив записей с полями id и text.")
        sys.exit(1)

    for r in records:
        if not isinstance(r, dict) or "id" not in r or "text" not in r:
            print(f"Неверный формат записи: {r}")
            sys.exit(1)

    client = get_qdrant()
    try:
        upsert(client, records)
        count = client.get_collection(COLLECTION_NAME).points_count
        print(f"Индексация завершена. Точек в коллекции: {count}")
    finally:
        client.close()


if __name__ == "__main__":
    main()
