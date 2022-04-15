from django.contrib import admin
from .models import Article, Category
from mptt.admin import MPTTModelAdmin


# Register your models here.
# admin.site.register(Article)
class CustomMPTTModelAdmin(MPTTModelAdmin):
    mptt_level_indent = 20


admin.site.register(Category, CustomMPTTModelAdmin)


@admin.register(Article)
class ArticleModel(admin.ModelAdmin):
    list_filter = ('id', 'title')
    list_display = ('id', 'title', 'description', 'category')
