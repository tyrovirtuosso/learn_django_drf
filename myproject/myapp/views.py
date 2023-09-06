from django.shortcuts import render, redirect
from .models import BlogPost
from .forms import ContactForm


def blog_post_list(request):
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

