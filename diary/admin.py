from django.contrib import admin

from .models import DiaryEntry


@admin.register(DiaryEntry)
class DiaryEntryAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "created_at", "mood")
    list_filter = ("author", "mood", "created_at")
    search_fields = ("title", "content")
