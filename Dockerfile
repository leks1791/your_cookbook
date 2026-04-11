# Используем официальный образ Python 3.11 slim (легкий и быстрый)
#FROM python:3.11-slim

# Устанавливаем рабочую директорию внутри контейнера
#WORKDIR /app

# Устанавливаем зависимости (делаем это ДО копирования кода, чтобы кэшировать слои)
#COPY requirements.txt .
#RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальной код проекта в контейнер
#COPY . .

# Открываем порт 8000
#EXPOSE 8000

# Команда запуска
#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .