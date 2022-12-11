from django.db import router
from django.urls import path, include
from .views import ArticleList, ArticleCreate, BlacklistTokenUpdateView, CategoryViewSet, UserDetails
from rest_framework.routers import DefaultRouter
from rest_framework_extensions.routers import ExtendedSimpleRouter
from django.conf.urls.static import static


router = DefaultRouter()
router.register('articles', ArticleList, basename='articles')
router.register('articalecreate', ArticleCreate, basename='articalecreate')
router.register('category', CategoryViewSet, basename='category')
# router.register('balcklist', BlacklistTokenUpdateView, basename='blacklist')


urlpatterns = [
    path('api/', include(router.urls)),
    path('api/accounts/', include('rest_registration.api.urls')),
    path('api/user/details', UserDetails.as_view()),
    path('api/blacklist/', BlacklistTokenUpdateView.as_view(),
         name='blacklist'),
     

]
