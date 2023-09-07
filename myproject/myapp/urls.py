from django.urls import path
from .views import blog_post_list, contact_view, success_page, profile, register, CustomLoginView, CustomLogoutView, unauthorized_page, PostCreateView, PostDetailView, PostListView, PostUpdateView, PostDeleteView

urlpatterns = [
    path('posts/', blog_post_list, name='blog_post_list'),
    path('contact/', contact_view, name='contact_view'),
    path('success/', success_page, name='success_page'),
    path('register/', register, name='register'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/login/', CustomLoginView.as_view(), name='login'), 
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('unauthorized/', unauthorized_page, name='unauthorized_page'),
    
    path('post/create/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/list/', PostListView.as_view(), name='post-list'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),


]
