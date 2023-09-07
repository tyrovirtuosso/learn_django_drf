from django.shortcuts import render, redirect
from .models import BlogPost, Post
from .forms import ContactForm, CustomUserCreationForm
from django.contrib.auth.forms import UserCreationForm

from django.urls import reverse_lazy 
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView,
)

# Views mainly for Post

# Handles creating new blog posts. It uses a form to input the title, content, and author.
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content']
    
    def form_valid(self, form):
        form.instance.author = self.request.user.username  # Set the author to the logged-in user's username
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('post-detail', args=[str(self.object.id)])
    
    

# Displays the details of a single blog post.
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['published_date']

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content']
    
    def form_valid(self, form):
        form.instance.author = self.request.user.username  # Set the author to the logged-in user's username
        return super().form_valid(form)

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = '/posts/list/'  # Redirect after successful deletion



# Views mainly for BlogPost

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

class CustomLogoutView(LogoutView):
    next_page = 'login'  # Redirect to the login page after logout
    
def unauthorized_page(request):
    return render(request, 'unauthorized.html')
    
@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

@permission_required('myapp.can_edit_content', login_url='/unauthorized/')
def blog_post_list(request):
    print("hello")
    posts = BlogPost.objects.all()
    context = {'posts': posts}
    return render(request, 'post_list.html', context)

def success_page(request):
    return render(request, 'success.html')

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the form data (e.g., send an email)
            return redirect('success_page') 
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.email = form.cleaned_data['email']
            user.save()
            print(user)
            # Get or create the 'All Users' group
            group, created = Group.objects.get_or_create(name='All Users')
            
            # Get the content type for the BlogPost model
            content_type = ContentType.objects.get_for_model(BlogPost)
            
            # Add permission to group            
            permission = Permission.objects.get(content_type=content_type, codename='can_edit_content')
            group.permissions.add(permission)

            # Add the user to the 'All Users' group
            # user.groups.add(group)
            
            login(request, user)  # Log the user in
            return redirect('profile')  # Redirect to user's profile
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})