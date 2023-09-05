from django.shortcuts import render
from .models import BlogPost

def blog_post_list(request):
    posts = BlogPost.objects.all()
    context = {'posts': posts}
    return render(request, 'post_list.html', context)
