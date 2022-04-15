from rest_framework import serializers
from .models import Category, Article
from django.utils.text import slugify


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        Model = Category
        fields = ['name', 'parent', 'slug']

    def get_fields(self):
        fields = super().get_fields()
        fields['children'] = CategorySerializer(many=True, read_only=True)
        return fields


class ArticleSerializer(serializers.ModelSerializer):
    title_slug = serializers.SerializerMethodField()

    def get_title_slug(self, instance):
        return slugify(instance.title)

    class Meta:
        model = Article
        fields = [
            'id', 'category', 'image', 'title', 'description', 'storie',
            'published', 'author', 'storie_positions', 'status', 'title_slug'
        ]
