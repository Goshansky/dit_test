# Мини-сервис семантического поиска

API на Python + Litestar для семантического поиска по данным. Векторная БД — Qdrant.

## Запуск

1. Поднять Qdrant:
   ```bash
   docker-compose up -d qdrant
   ```

2. Установить зависимости и запустить приложение локально:
   ```bash
   pip install -r requirements.txt
   uvicorn app.main:app --reload --host 0.0.0.0
   ```
