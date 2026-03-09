FROM python:3.13-slim

# Создаём рабочую директорию
WORKDIR /app

# Копируем файл с зависимостями
COPY requirements.txt /app/

# Устанавливаем зависимости напрямую через pip
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . /app/

# Создаём скрипт для запуска
RUN chmod +x /app/entrypoint.sh

# Открываем порт
EXPOSE 8000

# Запускаем приложение
CMD ["/app/entrypoint.sh"]