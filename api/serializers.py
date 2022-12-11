from typing_extensions import Required, Self
from rest_framework import serializers
from .models import Category, Article
from django.contrib.auth.models import User
from django.utils.text import slugify
from rest_framework_recursive.fields import RecursiveField


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for lowest level category that has no children."""

    parent = serializers.SerializerMethodField(source='get_parent')

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'parent', ]

    def get_parent(self, obj):
        if obj.parent:
            return obj.parent.name


# class CategorySerializer(serializers.Serializer):
#     # name = serializers.CharField()
#     # parent = serializers.CharField()
#     # slug = serializers.SlugField()
#     parent = serializers.SerializerMethodField(source='get_parent')
#     children = serializers.SerializerMethodField(source='get_children')

#     class Meta:
#         model = Category
#         fields = ['id', 'name', 'slug', 'parent', 'children', ]

#     def get_parent(self, obj):
#         if obj.parent:
#             return obj.parent.name

#     def get_children(self, obj):
#         if obj.children.exists():
#             children = [child for child in obj.children.all()]
#             children_with_children = [
#                 child for child in children if child.children.exists()]
#             children_without_children = [
#                 child for child in children if not child.children.exists()]
#             if children_with_children:
#                 return CategorySerializer(children_with_children, many=True).data
#             if children_without_children:
#                 return SubCategorySerializer(children_without_children, many=True).data


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
