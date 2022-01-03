from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.dashboard, name='blogs'),
    path('blogs', views.blogs, name='blogs'),
    path('add_article', views.add_article, name='add_article'),
    path('detail_article/<str:id>', views.detail_article, name='detail_article'),
    path('edit_article/<str:id>', views.edit_article, name='edit_article'),
    path('delete_article/<str:id>', views.delete_article, name='delete_article'),
    path('users', views.users, name="users"),

    # api
    path('api/articles/<str:x_api_key>', views.get_articles, name='get_articles'),
    path('api/article/<int:pk>/<str:x_api_key>', views.article_detail_api, name='article_detail_api'),
    path('api/add_article_api/<str:x_api_key>', views.add_article_api, name='add_article_api')
]