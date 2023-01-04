from rest_framework import serializers

from .models import NewsPost


class NewsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsPost
        fields = ["id", "title", "content", "article_id"]
