from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class DiaryEntry(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="entries")
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержание")
    created_at = models.DateTimeField(
        default=timezone.now, verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    mood = models.CharField(max_length=20, default="😐", verbose_name="Настроение")

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Diary entries"

    def __str__(self):
        return f"{self.title} - {self.author.username}"
