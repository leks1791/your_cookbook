# KODA.md — Контекст проекта Your Cook

## Обзор проекта

**Your Cook** — это веб-приложение для управления рецептами с поддержкой ролевой модели, системы модерации и публичного каталога рецептов.

### Назначение

Платформа позволяет пользователям:
- Создавать и управлять личными рецептами
- Публиковать рецепты для сообщества после модерации
- Просматривать одобренные рецепты в публичном каталоге
- Клонировать публичные рецепты в свой личный cookbook
- Участвовать в системе категорий и тегов

### Основные технологии

| Компонент | Технологии |
|-----------|------------|
| Backend | Python 3.11, FastAPI, SQLAlchemy, Alembic |
| Frontend | Vue 3, Vite, Pinia, Vue Router, TailwindCSS 4, PrimeVue 4 |
| База данных | PostgreSQL 16 (разработка: SQLite) |
| Контейнеризация | Docker, Docker Compose |
| Аутентификация | JWT (python-jose), bcrypt |

### Архитектура

```
project/
├── app/                    # Backend (FastAPI)
│   ├── models/            # SQLAlchemy модели
│   ├── routers/           # API роутеры
│   ├── schemas/           # Pydantic схемы
│   ├── services/          # Бизнес-логика
│   ├── auth.py            # Аутентификация и авторизация
│   ├── database.py        # Подключение к БД
│   ├── main.py            # Entry point приложения
│   └── settings.py        # Конфигурация
├── frontend/              # Frontend (Vue 3)
│   ├── src/
│   │   ├── components/    # Vue компоненты
│   │   ├── views/         # Страницы приложения
│   │   ├── stores/        # Pinia стейт-менеджмент
│   │   ├── router/        # Vue Router конфигурация
│   │   └── api.js         # API клиент (axios)
│   └── vite.config.js     # Конфигурация Vite
├── tests/                 # Backend тесты
└── docker-compose.yml     # Оркестрация контейнеров
```

## Сборка и запуск

### Предварительные требования

- Docker и Docker Compose
- Python 3.11+ (для локальной разработки без Docker)
- Node.js 18+ (для локальной разработки frontend без Docker)

### Запуск через Docker Compose (рекомендуется)

```bash
# Запуск всех сервисов (backend, frontend, PostgreSQL)
docker-compose up --build

# Остановка сервисов
docker-compose down

# Запуск тестов
docker-compose run backend pytest
```

### Локальный запуск Backend

```bash
# Создание виртуального окружения
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Установка зависимостей
pip install -r requirements.txt

# Запуск сервера разработки
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Локальный запуск Frontend

```bash
cd frontend

# Установка зависимостей
npm install

# Запуск сервера разработки
npm run dev

# Сборка для продакшена
npm run build
```

### Управление миграциями базы данных

```bash
# Создание новой миграции
alembic revision --autogenerate -m "description"

# Применение миграций
alembic upgrade head

# Откат миграции
alembic downgrade -1
```

## API Endpoints

### Аутентификация (`/auth`)

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| POST | `/auth/register` | Регистрация пользователя |
| POST | `/auth/login` | Вход в систему |
| GET | `/auth/me` | Получение данных текущего пользователя |

### Рецепты (`/recipes`)

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| GET | `/recipes` | Получение списка рецептов пользователя |
| GET | `/recipes/{id}` | Получение рецепта по ID |
| POST | `/recipes` | Создание нового рецепта |
| PUT | `/recipes/{id}` | Обновление рецепта |
| DELETE | `/recipes/{id}` | Удаление рецепта |
| POST | `/recipes/{id}/submit-for-review` | Отправка рецепта на модерацию |

### Каталог (`/catalog`)

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| GET | `/catalog` | Получение списка публичных рецептов |
| GET | `/catalog/{id}` | Получение публичного рецепта |
| POST | `/catalog/{id}/clone` | Клонирование рецепта в личный cookbook |

### Админ-панель (`/admin`)

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| GET | `/admin/recipes/pending` | Получение рецептов на модерации |
| POST | `/admin/recipes/{id}/approve` | Одобрение рецепта |
| POST | `/admin/recipes/{id}/reject` | Отклонение рецепта |
| POST | `/admin/recipes` | Создание рецепта от имени администратора |

### Категории (`/categories`)

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| GET | `/categories` | Получение списка категорий |
| POST | `/categories` | Создание категории |
| PUT | `/categories/{id}` | Обновление категории |
| DELETE | `/categories/{id}` | Удаление категории |

## Ролевая модель

### Роли пользователей

| Роль | Описание | Доступы |
|------|----------|---------|
| `user` | Обычный пользователь | Создание/редактирование личных рецептов, отправка на модерацию, просмотр каталога |
| `admin` | Администратор | Все возможности пользователя + модерация рецептов, управление категориями |

### Статусы публикации рецепта

| Статус | Описание | Видимость |
|--------|----------|-----------|
| `draft` | Черновик | Только владелец |
| `pending` | На модерации | Только владелец и администраторы |
| `approved` | Одобрен | Публичный каталог |
| `rejected` | Отклонён | Только владелец |

## Структура данных

### Модель Recipe

Основные поля:
- `title` — Название рецепта
- `description` — Описание
- `ingredients` — Ингредиенты (JSON)
- `steps` — Шаги приготовления (JSON)
- `tags` — Теги (JSON)
- `photos` — Фотографии (JSON)
- `prep_time` — Время подготовки (мин)
- `cook_time` — Время готовки (мин)
- `servings` — Количество порций
- `difficulty` — Сложность
- `cuisine` — Тип кухни
- `visibility` — Видимость (`private`/`public`)
- `publication_status` — Статус публикации (`draft`/`pending`/`approved`/`rejected`)
- `is_admin_recipe` — Флаг рецепта администратора
- `approved_by` — ID администратора, одобвившего рецепт
- `approved_at` — Дата одобрения
- `rejection_reason` — Причина отклонения
- `original_recipe_id` — ID исходного рецепта (для клонированных)

### Модель User

Основные поля:
- `username` — Имя пользователя
- `email` — Email адрес
- `hashed_password` — Хеш пароля (bcrypt)
- `role` — Роль (`user`/`admin`)

## Правила разработки

### Backend

- **Код-стиль:** Ruff (line-length: 100, double quotes, space indent)
- **Типизация:** Pydantic схемы для валидации данных
- **Базы данных:** SQLAlchemy с Alembic для миграций
- **Логирование:** Модуль `logging` с информативными сообщениями
- **Обработка ошибок:** HTTPException с подходящими статус-кодами

### Frontend

- **Компоненты:** Vue 3 с `<script setup>` синтаксисом
- **UI-библиотека:** PrimeVue 3 (Button, DataTable, Dialog, Toast, Dropdown, Card, TabView, Tag и др.)
- **Стейт-менеджмент:** Pinia stores
- **Роутинг:** Vue Router с meta-полями для защиты маршрутов
- **API клиент:** Axios с базовой конфигурацией в `api.js`
- **Стилизация:** TailwindCSS 4 + PrimeVue Aura тема
- **Иконки:** PrimeIcons

**PrimeVue компоненты (используются в проекте):**
- Импортируются индивидуально в каждом компоненте
- Тема: Aura Light Blue (`aura-light-blue/theme.css`)
- Основные компоненты:
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

**Пример импорта:**
```vue
<script setup>
import Button from 'primevue/button'
import Dialog from 'primevue/dialog'
import { useToast } from 'primevue/usetoast'
</script>
```

**PrimeIcons (основные иконки):**

| Иконка | Описание | Использование |
|--------|----------|---------------|
| `pi-home` | Дом | Главная, дашборд |
| `pi-book` | Книга | Рецепты |
| `pi-folder` | Папка | Категории, подборки |
| `pi-heart` | Сердце | Избранное |
| `pi-tags` | Теги | Теги рецептов |
| `pi-shield` | Щит | Админ-панель |
| `pi-sign-out` | Выход | Выход из аккаунта |
| `pi-sign-in` | Вход | Вход в аккаунт |
| `pi-user` | Пользователь | Профиль |
| `pi-plus` | Добавить | Создание рецептов |
| `pi-trash` | Удалить | Удаление элементов |
| `pi-pencil` | Редактировать | Редактирование |
| `pi-search` | Поиск | Поиск рецептов |
| `pi-shopping-cart` | Корзина | Список покупок |
| `pi-clock` | Время | Время готовки |
| `pi-check` | Галочка | Подтверждение |
| `pi-times` | Крестик | Отмена |
| `pi-images` | Фотографии | Галерея рецептов |

**Использование иконок:**
```html
<i class="pi pi-plus"></i>
<i class="pi pi-shopping-cart text-2xl text-orange-500"></i>
```

### Тестирование

- Backend: pytest с httpx для тестирования API
- Тесты размещаются в `tests/` директории
- Запуск: `docker-compose run backend pytest`

### Git-практики

- Используйте семантические сообщения коммитов
- Создавайте feature-ветки от `main`
- Проводите code review перед мержем
- Обновляйте миграции при изменениях схемы БД

## Конфигурация

### Переменные окружения Backend

Создайте `.env` файл на основе `.env.example`:

```env
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname
SECRET_KEY=your-secret-key-min-32-chars
ACCESS_TOKEN_EXPIRE_DAYS=7
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

### Переменные окружения Frontend

Создайте `.env` файл в `frontend/` на основе `frontend/.env.example`:

```env
VITE_API_BASE_URL=http://localhost:8000
```

## Создание администратора

Для создания администратора можно использовать один из способов:

1. **Скрипт создания:**
   ```bash
   python scripts/create_admin.py
   ```

2. **SQL-скрипт:**
   ```bash
   psql -U your_cook_user -d your_cook_db -f make_admin.sql
   ```

3. **Через API:**
   - Зарегистрируйте пользователя через `/auth/register`
   - Измените роль в базе данных вручную

## Проверка здоровья

```bash
curl http://localhost:8000/health
# Ответ: {"status": "ok"}
```

## Текущий статус реализации

- [x] Регистрация и аутентификация пользователей
- [x] Ролевая модель (user/admin)
- [x] CRUD операций с рецептами
- [x] Система категорий
- [x] Публикация рецептов и модерация
- [x] Публичный каталог рецептов
- [x] Клонирование рецептов из каталога
- [x] Админ-панель для модерации
- [ ] Поиск и фильтры в каталоге
- [ ] Frontend-тесты
- [ ] Улучшение рендеринга ингредиентов и шагов

## Полезные команды

```bash
# Запуск всех сервисов
docker-compose up --build

# Просмотр логов backend
docker-compose logs -f backend

# Выполнение команды в backend контейнере
docker-compose exec backend bash

# Сброс базы данных
docker-compose down -v && docker-compose up --build

# Запуск тестов с подробным выводом
docker-compose run backend pytest -v

# Проверка линтером
docker-compose run backend ruff check .
docker-compose run backend ruff format --check .
```

## Заметки

- JWT токены истекают через 7 дней по умолчанию
- CORS настроен для localhost:5173, 5174, 5175, 3000
- Пароли хешируются с использованием bcrypt
- База данных по умолчанию — SQLite, для продакшена используйте PostgreSQL
