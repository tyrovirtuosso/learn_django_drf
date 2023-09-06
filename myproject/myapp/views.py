from django.shortcuts import render, redirect
from .models import BlogPost
from .forms import ContactForm, CustomUserCreationForm
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType



class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

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