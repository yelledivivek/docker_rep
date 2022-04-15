from itertools import permutations
from django.shortcuts import render
from .models import Category, Article
from .serializers import CategorySerializer, ArticleSerializer
from rest_framework import viewsets
from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticated


class StaffPermissio(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff

    # def has_object_permission(self, request, view, obj):
    #     if request.method in SAFE_METHODS:
    #         return True

    #     return request.user.is_staff


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ArticleList(viewsets.ReadOnlyModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filterset_fields = ['category', 'storie_positions']
    search_fields = ['$title', '$description']


class ArticleCreate(viewsets.ModelViewSet, StaffPermissio):
    permission_classes = [StaffPermissio]
    queryset = Article.postobjects.all()
    serializer_class = ArticleSerializer


# Create your views here.
