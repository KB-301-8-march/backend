# Используем официальный образ Python
FROM python:3.10-slim

# Установка рабочей директории в контейнере
WORKDIR /app

# Скопировать файл зависимостей в рабочую директорию
COPY requirements.txt .

# Установка зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы вашего приложения в контейнер
COPY . .

# Указываем команду по умолчанию для запуска FastAPI-приложения
# При необходимости замените 'main:app' на 'filename:app' вашего проекта
CMD ["uvicorn", "main:app", "--reload"]