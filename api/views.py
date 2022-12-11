from django.shortcuts import render
from rest_framework.pagination import LimitOffsetPagination
from .models import Category, Article
from .serializers import CategorySerializer, ArticleSerializer
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework import viewsets
from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken



class StaffPermissio(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff

    # def has_object_permission(self, request, view, obj):
    #     if request.method in SAFE_METHODS:
    #         return True

    #     return request.user.is_staff


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer

    def get_queryset(self):
        queryset = Category.objects.filter(level=0)
        return queryset

    
# class CategoryFilter(django_filters.FilterSet):
#     class Meta:
#         model = Category
#         fields = ['parent']


class ArticleList(viewsets.ReadOnlyModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    pagination_class = LimitOffsetPagination
    filterset_fields = ['category', 'storie_positions']
    search_fields = ['$title', '$description']

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        parent = self.request.query_params.get('parent', None)

        if parent is not None:
            queryset = queryset.filter(category__parent=parent)
        return super().filter_queryset(queryset)


class ArticleCreate(viewsets.ModelViewSet, StaffPermissio):
    permission_classes = [StaffPermissio]
    queryset = Article.postobjects.all()
    serializer_class = ArticleSerializer


class BlacklistTokenUpdateView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class UserDetails(APIView):
    def get(self, request, format=None):
        try:
            user = request.user
            user = UserSerializer(user)

            return Response(
                {'user': user.data},
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                {'error': 'Something went wrong when trying to load user'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

