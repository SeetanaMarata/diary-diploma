from django.contrib.auth.models import User
from rest_framework import serializers

from .models import DiaryEntry


class DiaryEntrySerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = DiaryEntry
        fields = [
            "id",
            "author",
            "author_name",
            "title",
            "content",
            "created_at",
            "updated_at",
            "mood",
        ]
        read_only_fields = ["id", "author", "created_at", "updated_at"]

    def create(self, validated_data):
        validated_data["author"] = self.context["request"].user
        return super().create(validated_data)
