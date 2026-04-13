# 🍳 CookBook AI

Современное веб-приложение для управления рецептами с поддержкой категорий, авторизации и статистики.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![Vue](https://img.shields.io/badge/Vue-3.x-green.svg)](https://vuejs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-brightgreen.svg)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📋 Содержание

- [Технологии](#-технологии)
- [Быстрый старт](#-быстрый-старт)
- [Docker](#-docker-рекомендуемый-способ)
- [Локальная установка](#-локальная-установка)
- [API Endpoints](#api-endpoints)
- [Безопасность](#-безопасность)
- [Тестирование](#-тестирование)

---

## 🛠 Технологии

### Backend
- **FastAPI** — современный асинхронный фреймворк для API
- **SQLAlchemy 2.0** — ORM для работы с базой данных
- **Alembic** — миграции базы данных
- **Pydantic v2** — валидация данных
- **JWT (python-jose)** — аутентификация
- **Passlib + bcrypt** — хеширование паролей
- **Ruff** — линтер и форматтер кода

### Frontend
- **Vue 3** — прогрессивный JS-фреймворк
- **Vite** — быстрый сборщик
- **Pinia** — управление состоянием
- **Vue Router 5** — маршрутизация с guard'ами
- **Axios** — HTTP-клиент с interceptors (автоматическая обработка 401)
- **Tailwind CSS v4** — утилитарные стили

### База данных
- **SQLite** (по умолчанию для разработки)
- Поддержка **PostgreSQL** для продакшена

---

## 🚀 Быстрый старт

### Предварительные требования
- Python 3.11+
- Node.js 18+
- **Docker & Docker Compose** (рекомендуемый способ)
- **Make** (опционально, для удобных команд)

---

## 🐳 Docker (рекомендуемый способ)

### Запуск всего проекта

```bash
# Запустить backend и frontend в режиме разработки
docker-compose up

# Запустить в фоновом режиме
docker-compose up -d

# Остановить контейнеры
docker-compose down
```

### Только Backend

```bash
docker-compose up backend
```

### Только Frontend

```bash
docker-compose up frontend
```

### Пересобрать образы

```bash
docker-compose build --no-cache
docker-compose up
```

### Доступ к приложению

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs

---

## ⚙️ Makefile (удобные команды)

Проект включает Makefile для быстрого запуска:

```bash
# Запустить проект
make up

# Остановить проект
make down

# Запустить тесты
make test
```

---


### Доступ к приложению

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation (Swagger)**: http://localhost:8000/docs
- **Alternative API Docs (ReDoc)**: http://localhost:8000/redoc

---

## 🔌 API Endpoints

### Основные возможности

#### 📝 Расширенная форма создания рецептов

Создавайте богатые рецепты с помощью удобной формы:

- **Базовая информация**: Название, описание, кухня, сложность
- **Время**: Подготовка и приготовление отдельно
- **Порции**: Количество порций
- **Категории**: Множественный выбор из существующих категорий с цветовой индикацией
- **Теги**: Множественный выбор + создание новых тегов на лету
- **Ингредиенты**: Динамический список с добавлением/удалением/переупорядочиванием
  - Поддержка быстрого ввода через запятую
  - Отдельные поля: количество, единица измерения, название
- **Шаги приготовления**: 
  - Drag & drop для изменения порядка
  - Каждый шаг может иметь опциональный таймер
- **Фото**: 
  - Загрузка нескольких фото
  - Drag & drop загрузка
  - Предпросмотр
  - Переупорядочивание
  - Выбор обложки
- **Заметки**: Дополнительные советы и заметки

---

### Authentication (`/auth`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Регистрация нового пользователя |
| POST | `/auth/login` | Вход (возвращает JWT токен) |
| GET | `/auth/me` | Получить данные текущего пользователя |

### Recipes (`/recipes`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/recipes` | Получить список рецептов (пагинация) |
| POST | `/recipes` | Создать новый рецепт |
| GET | `/recipes/{id}` | Получить рецепт по ID |
| PUT | `/recipes/{id}` | Обновить рецепт |
| DELETE | `/recipes/{id}` | Удалить рецепт |
| GET | `/recipes/stats` | Получить статистику рецептов |

**Поля рецепта:**
- `title` — Название рецепта
- `description` — Описание
- `ingredients` — JSON строка с ингредиентами (массив объектов: `{amount, unit, name}`)
- `steps` — JSON строка со шагами приготовления (массив объектов: `{order, description, timer_seconds}`)
- `tags` — Массив тегов (например: `["Завтрак", "Быстро"]`)
- `photos` — Массив URL фото
- `prep_time` — Время подготовки (минуты)
- `cook_time` — Время приготовления (минуты)
- `servings` — Количество порций
- `difficulty` — Сложность: `easy`, `medium`, `hard`
- `cuisine` — Тип кухни (например: "Итальянская")
- `notes` — Дополнительные заметки
- `category_ids` — Массив ID категорий (например: `[1, 2, 5])

**Пример запроса POST /recipes:**
```json
{
  "title": "Домашняя паста карбонара",
  "description": "Классическая итальянская паста",
  "ingredients": "[{\"amount\": \"400\", \"unit\": \"г\", \"name\": \"спагетти\"}, {\"amount\": \"200\", \"unit\": \"г\", \"name\": \"бекон\"}]",
  "category_ids": [1, 3]
}
```

**Ответ включает категории:**
```json
{
  "id": 1,
  "title": "Домашняя паста карбонара",
  "categories": [
    {"id": 1, "name": "Итальянская кухня", "color": "#f97316"},
    {"id": 3, "name": "Быстрые блюда", "color": "#10b981"}
  ]
}
```

### Categories (`/categories`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/categories` | Получить список категорий |
| POST | `/categories` | Создать новую категорию |
| GET | `/categories/{id}` | Получить категорию по ID |
| PUT | `/categories/{id}` | Обновить категорию |
| DELETE | `/categories/{id}` | Удалить категорию |

**Примечание**: Поле `color` требует валидный HEX код (например, `#f97316`). Нельзя удалить категорию, если к ней привязаны рецепты.

### System
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Проверка здоровья сервиса |

---

## 🔒 Безопасность

### Реализовано
- ✅ Хеширование паролей с bcrypt
- ✅ JWT токены для аутентификации
- ✅ Защита маршрутов через `get_current_user`
- ✅ Проверка владельца при обновлении/удалении
- ✅ Валидация пароля (минимум 6 символов)
- ✅ Email валидация через Pydantic

### Рекомендации для продакшена
1. **SECRET_KEY**: Заменить на случайную строку минимум 32 символа
2. **HTTPS**: Использовать SSL/TLS сертификаты
3. **PostgreSQL**: Переключиться с SQLite на PostgreSQL
4. **Rate limiting**: Добавить ограничение запросов
5. **CORS**: Настроить строгий список разрешённых доменов

---

## 🧪 Тестирование

### Запуск тестов

```bash
# Backend тесты
pytest tests/ -v

# С покрытием
pytest tests/ --cov=app --cov-report=html

# Через Makefile
make test
```

### Линтинг

```bash
# Backend (Ruff)
ruff check app/
ruff format app/

# Frontend
cd frontend
npm run lint
```

---

## 📝 Лицензия

MIT License. См. файл LICENSE для деталей.

