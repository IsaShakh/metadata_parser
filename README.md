# Metadata Parser
Проект на FastAPI для парсинга метаданных файлов через внешний сервис(в данном случае exif.tools).

## Summary
- Загрузка файлов любого типа;
- Извлечение метаданных;
- Сохранение результатов в БД и JSON-файл;
- Фильтрация сохраненных данных.

## Stack
- FastAPI;
- SQLAlchemy;
- PostgreSQL;
- Alembic;
- httpx, bs4;
- Docker, docker-compose;

## Старт
### 1. Клонирование репозитория 

### 2. Создайте .env в корне проекта и заполните на основе примера:
```bash
POSTGRES_USER=user
POSTGRES_PASSWORD=pass
POSTGRES_DB=db
DATABASE_URL=postgresql+asyncpg://user:pass@db:5432/db
```

### 3. Запустите проект через Docker Compose:
```bash
docker-compose up --build
```

### 4. Проверка работы через Swagger:
```bash
http://localhost:8000/docs
```

## Миграции БД

