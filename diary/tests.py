from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from .models import DiaryEntry


class DiaryTestCase(TestCase):
    def setUp(self):
        """Создаём тестового пользователя перед каждым тестом"""
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.client = APIClient()

    def test_user_registration(self):
        """Тест регистрации нового пользователя"""
        response = self.client.post(
            "/register/",
            {
                "username": "newuser",
                "password1": "newpass123",
                "password2": "newpass123",
            },
        )
        self.assertEqual(response.status_code, 302)  # Редирект после регистрации
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_user_login(self):
        """Тест входа пользователя"""
        response = self.client.post(
            "/login/", {"username": "testuser", "password": "testpass123"}
        )
        self.assertEqual(response.status_code, 302)  # Редирект после входа

    def test_create_entry(self):
        """Тест создания записи в дневнике"""
        # Сначала авторизуемся
        self.client.login(username="testuser", password="testpass123")

        # Создаём запись
        response = self.client.post(
            "/dashboard/",
            {
                "title": "Тестовая запись",
                "content": "Содержание тестовой записи",
                "mood": "😊",
            },
        )
        self.assertEqual(response.status_code, 302)  # Редирект после создания

        # Проверяем, что запись создалась
        entry = DiaryEntry.objects.first()
        self.assertEqual(entry.title, "Тестовая запись")
        self.assertEqual(entry.author, self.user)

    def test_api_jwt_token(self):
        """Тест получения JWT токена через API"""
        response = self.client.post(
            "/api/token/", {"username": "testuser", "password": "testpass123"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_api_entries_without_token(self):
        """Тест доступа к API без токена (должен быть запрещён)"""
        response = self.client.get("/api/entries/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_entry(self):
        """Тест удаления записи"""
        self.client.login(username="testuser", password="testpass123")

        # Создаём запись
        entry = DiaryEntry.objects.create(
            author=self.user, title="Для удаления", content="Будет удалена"
        )

        # Удаляем
        response = self.client.post("/dashboard/", {"delete_id": entry.id})
        self.assertEqual(response.status_code, 302)

        # Проверяем, что запись удалилась
        self.assertFalse(DiaryEntry.objects.filter(id=entry.id).exists())
