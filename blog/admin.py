from django.contrib import admin
from . models import Category, Article

# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'body', 'category', 'date')

admin.site.register(Category)
admin.site.register(Article, ArticleAdmin)