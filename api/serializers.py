from typing_extensions import Self
from rest_framework import serializers
from .models import Category, Article
from django.contrib.auth.models import User
from django.utils.text import slugify
from rest_framework_recursive.fields import RecursiveField


class CategorySerializer(serializers.Serializer):
    name = serializers.CharField()
    parent = serializers.CharField()
    slug = serializers.SlugField()
    # class Meta:
    #     Model = Category
    #     fields = ['name', 'parent', 'slug']
        
    # def get_fields(self):
    #     fields = super(CategorySerializer, self).get_fields()
    #     fields['children'] = CategorySerializer(many=True, read_only=True)
    #     return fields


class ArticleSerializer(serializers.ModelSerializer):
    title_slug = serializers.SerializerMethodField()
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    category = CategorySerializer()

    def get_title_slug(self, instance):
        return slugify(instance.title)

    class Meta:
        model = Article
        fields = [
            'id', 'category', 'image', 'title', 'description', 'storie',
            'published', 'author', 'storie_positions', 'status', 'title_slug'
        ]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'is_staff', 'username', )

