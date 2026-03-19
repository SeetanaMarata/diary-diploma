#!/bin/sh

# Ждём, пока PostgreSQL запустится
echo "Waiting for PostgreSQL..."
while ! nc -z db 5432; do
  sleep 0.5
done
echo "PostgreSQL started"

# Применяем миграции
python manage.py migrate

# Запускаем сервер
python manage.py runserver 0.0.0.0:8000