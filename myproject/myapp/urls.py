from django.urls import path
from .views import blog_post_list

urlpatterns = [
    path('posts/', blog_post_list, name='blog_post_list'),
]
