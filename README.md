# Your Cook

Your Cook — это full-stack приложение для управления рецептами с аутентификацией, ролевой моделью, системой модерации и публичным каталогом.

## Обзор проекта

**Your Cook** — веб-приложение, которое позволяет пользователям:
- Создавать и управлять личными рецептами
- Публиковать рецепты для сообщества после модерации
- Просматривать одобренные рецепты в публичном каталоге
- Клонировать публичные рецепты в свой личный cookbook
- Участвовать в системе категорий и тегов

### Архитектура

- `app/` — FastAPI backend (Python 3.11)
- `frontend/` — Vue 3 + Vite frontend
- `tests/` — backend тесты с pytest
- `app/alembic/` — миграции базы данных

## Стек технологий

| Компонент | Технологии |
|-----------|------------|
| Backend | Python 3.11, FastAPI, SQLAlchemy 2, Pydantic 2, Alembic |
| Frontend | Vue 3, Pinia, Vue Router, Vite, TailwindCSS 4, PrimeVue 3 |
| Аутентификация | JWT (python-jose), bcrypt |
| База данных | PostgreSQL 16 (разработка: SQLite) |
| Контейнеризация | Docker, Docker Compose |
| UI-компоненты | PrimeVue 3.52.0 (Aura Light Blue тема) |
| Иконки | PrimeIcons 7.0.0 |

## Основные возможности

### Аутентификация и авторизация
- Регистрация и вход пользователей
- JWT токены с истекающим сроком действия (7 дней по умолчанию)
- Ролевая модель: `user` и `admin`

### Управление рецептами
- Создание, редактирование и удаление личных рецептов
- Черновики, отправка на модерацию
- Статусы: `draft`, `pending`, `approved`, `rejected`
- Ингредиенты и шаги приготовления
- Теги и категории
- Фотографии рецептов
- Время приготовления, порции, сложность

### Публичный каталог
- Просмотр одобренных рецептов
- Фильтрация по категориям и тегам
- Клонирование рецептов из каталога в личный cookbook

### Админ-панель
- Модерация рецептов (одобрение/отклонение)
- Управление категориями
- Создание рецептов от имени администратора

### UI/UX
- Адаптивный дизайн с TailwindCSS 4
- PrimeVue компоненты (Button, Card, Dialog, DataTable, Toast и др.)
- PrimeIcons иконки
- Горячая перезагрузка (HMR) при разработке

## Требования

- **Python 3.11+**
- **Node.js 18+**
- **Docker & Docker Compose** (рекомендуется)
- **PostgreSQL 16** (для production)

## Быстрый старт

### Вариант 1: Docker (рекомендуется)

```bash
# Запуск всех сервисов
docker-compose up --build

# Остановка
docker-compose down

# Сброс базы данных
docker-compose down -v && docker-compose up --build
```

### Вариант 2: Локальная разработка

#### 1. Backend setup

Создайте `.env` в корне проекта:

```env
DATABASE_URL=postgresql://your_cook_user:your_cook_pass@localhost:5432/your_cook_db
SECRET_KEY=your-secret-key-min-32-chars
ACCESS_TOKEN_EXPIRE_DAYS=7
CORS_ORIGINS=["http://localhost:5173","http://localhost:5174","http://localhost:5175","http://localhost:3000"]
```

Установка зависимостей:

```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

pip install -r requirements.txt
```

Миграции базы данных:

```bash
alembic upgrade head
```

Запуск backend:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Backend URLs:**
- API: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- Health check: `http://localhost:8000/health`

#### 2. Frontend setup

Создайте `frontend/.env`:

```env
VITE_API_BASE_URL=http://localhost:8000
```

Установка зависимостей и запуск:

```bash
cd frontend
npm install
npm run dev
```

**Frontend URL:** `http://localhost:5173`

#### Hot-reload

Vite настроен с polling для корректной работы в Docker:
- Изменения в `.vue`, `.js`, `.css` файлах применяются автоматически
- Браузер обновляется без перезагрузки страницы (HMR)

## Docker

Полная конфигурация в `docker-compose.yml`:

```bash
# Запуск всех сервисов
docker-compose up --build

# Фоновый режим
docker-compose up -d

# Логи
docker-compose logs -f frontend
docker-compose logs -f backend

# Остановка
docker-compose down

# Пересборка без кэша
docker-compose build --no-cache
```

### Управление контейнерами

```bash
# Выполнение команд в контейнере
docker-compose exec backend bash
docker-compose exec frontend bash

# Запуск тестов
docker-compose run backend pytest -v

# Проверка линтером
docker-compose run backend ruff check .
```

## Тестирование

### Backend тесты

```bash
# Локально
python -m pytest -v

# В Docker
docker-compose run backend pytest -v
```

### Frontend тесты

В процессе реализации...

## Полезные команды

### Backend

```bash
# Линтер и форматирование
ruff check app tests
ruff format app tests

# Создание миграции
alembic revision --autogenerate -m "description"

# Применение миграций
alembic upgrade head

# Откат миграции
alembic downgrade -1
```

### Frontend

```bash
# Разработка
npm run dev

# Production build
npm run build

# Проверка
npm run preview
```

## API Overview

### Аутентификация (`/auth`)

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| POST | `/auth/register` | Регистрация пользователя |
| POST | `/auth/login` | Вход в систему |
| GET | `/auth/me` | Данные текущего пользователя |

### Рецепты (`/recipes`)

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| GET | `/recipes` | Список рецептов пользователя |
| GET | `/recipes/{id}` | Рецепт по ID |
| POST | `/recipes` | Создание рецепта |
| PUT | `/recipes/{id}` | Обновление рецепта |
| DELETE | `/recipes/{id}` | Удаление рецепта |
| POST | `/recipes/{id}/submit-for-review` | Отправка на модерацию |

### Каталог (`/catalog`)

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| GET | `/catalog` | Публичные рецепты |
| GET | `/catalog/{id}` | Публичный рецепт |
| POST | `/catalog/{id}/clone` | Клонирование рецепта |

### Админ-панель (`/admin`)

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| GET | `/admin/recipes/pending` | Рецепты на модерации |
| POST | `/admin/recipes/{id}/approve` | Одобрить рецепт |
| POST | `/admin/recipes/{id}/reject` | Отклонить рецепт |
| POST | `/admin/recipes` | Создание рецепта админом |

### Категории (`/categories`)

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| GET | `/categories` | Список категорий |
| POST | `/categories` | Создание категории |
| PUT | `/categories/{id}` | Обновление категории |
| DELETE | `/categories/{id}` | Удаление категории |

## Ролевая модель

| Роль | Описание | Доступы |
|------|----------|---------|
| `user` | Обычный пользователь | CRUD рецептов, отправка на модерацию, каталог |
| `admin` | Администратор | Все возможности user + модерация, управление категориями |

## Статусы рецептов

| Статус | Описание | Видимость |
|--------|----------|-----------|
| `draft` | Черновик | Только владелец |
| `pending` | На модерации | Владелец и админы |
| `approved` | Одобрен | Публичный каталог |
| `rejected` | Отклонён | Только владелец |

## Создание администратора

### Способ 1: Скрипт

```bash
python scripts/create_admin.py
```

### Способ 2: SQL

```bash
psql -U your_cook_user -d your_cook_db -f make_admin.sql
```

### Способ 3: Через API

1. Зарегистрируйтесь через `/auth/register`
2. Измените роль в базе данных вручную на `admin`

## Конфигурация

### Backend переменные окружения

```env
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname
SECRET_KEY=your-secret-key-min-32-chars
ACCESS_TOKEN_EXPIRE_DAYS=7
CORS_ORIGINS=["http://localhost:5173","http://localhost:5174","http://localhost:5175","http://localhost:3000"]
```

### Frontend переменные окружения

```env
VITE_API_BASE_URL=http://localhost:8000
```

## PrimeVue компоненты

Используемые компоненты:
- `Button` — кнопки действий
- `Card` — карточки
- `Dialog` — модальные окна
- `DataTable` — таблицы данных
- `Dropdown` — выпадающие списки
- `InputText/InputNumber` — поля ввода
- `Toast` — уведомления
- `Tag` — метки/теги
- `TabView` — вкладки
- `Badge` — бейджи
- `ProgressSpinner` — индикаторы загрузки

## Примечания

- JWT токены истекают через 7 дней по умолчанию
- CORS настроен для localhost:5173, 5174, 5175, 3000
- Пароли хешируются с использованием bcrypt
- База данных по умолчанию — SQLite, для production используйте PostgreSQL
- Hot-reload работает через polling в Docker
- TailwindCSS 4 с PrimeVue Aura Light Blue темой

## License

MIT
