from django.urls import path
from .views import blog_post_list, contact_view, success_page, profile, register, CustomLoginView, CustomLogoutView, unauthorized_page

urlpatterns = [
    path('posts/', blog_post_list, name='blog_post_list'),
    path('contact/', contact_view, name='contact_view'),
    path('success/', success_page, name='success_page'),
    path('register/', register, name='register'),
    path('accounts/profile/', profile, name='profile'),
    path('login/', CustomLoginView.as_view(), name='login'), 
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('unauthorized/', unauthorized_page, name='unauthorized_page'),


]
