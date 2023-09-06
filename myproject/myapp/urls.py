from django.urls import path
from .views import blog_post_list, contact_view, success_page

urlpatterns = [
    path('posts/', blog_post_list, name='blog_post_list'),
    path('contact/', contact_view, name='contact_view'),
    path('success/', success_page, name='success_page'),
]
