from django.db import router
from django.urls import path, include
from .views import ArticleList, ArticleCreate
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static


router = DefaultRouter()
router.register('articles', ArticleList, basename='articles')
router.register('articalecreate', ArticleCreate, basename='articalecreate')


urlpatterns = [
    path('api/', include(router.urls)),

]
