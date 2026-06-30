FROM python:3.13-slim

# Устанавливаем переменные окружения, чтобы Python не буферизировал логи
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Создаем рабочую директорию внутри контейнера
WORKDIR /app

# Устанавливаем системные зависимости (нужны для некоторых библиотек Python)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем файл зависимостей
COPY requirements.txt /app/

# Обновляем pip и устанавливаем библиотеки
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Копируем весь код бэкенда в контейнер
COPY . /app/