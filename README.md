# learn_django_drf

## Set up your Django development environment 
This repo will be used to famillirize myself with Django and Django Rest Framework(DRF)

**Package:** ```pip install Django python-dotenv```

**To create Django Project:** ```django-admin startproject myproject```

**To create Django App within Project:** ```python manage.py startapp myapp```

**Add the App to INSTALLED_APPS:** Open your project's settings.py file (myproject/settings.py) and add your app to the INSTALLED_APPS list. Make sure to include the name of the app as a Python path relative to the project's root. 

```
INSTALLED_APPS = [
    # ...
    'myapp',
]
```

**Directory Structure:** 
- myproject/: This is the project's root directory.
    - manage.py: A command-line utility to manage various aspects of your Django project.
    - myproject/: This is the actual Python package for your project.
        - __init__.py: An empty file that tells Python this directory should be considered a Python package.
        - settings.py: Configuration settings for your project.
        - urls.py: URL routing for your project.
        - asgi.py and wsgi.py: Entry points for ASGI and WSGI servers (used for deployment).
    - myapp/:
    - venv/ (or env/): This is a virtual environment (if you created one) to isolate your project's dependencies.

**To Run the Development Server:**
```python manage.py runserver```

**To connect to cloud database(PostgreSQL):**

- Install PostgreSQL adapter for Django:
```pip install psycopg2-binary```

- Configure Database Settings:
 In your Django project's settings.py file, you'll need to configure the database settings with the AWS PostgreSQL connection details. Replace the placeholders with your actual database information:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'your_db_name',
        'USER': 'your_db_username',
        'PASSWORD': 'your_db_password',
        'HOST': 'your_db_host_endpoint',
        'PORT': 'your_db_port',
    } 
}
```

**Creating an admin superuser:** ```python manage.py createsuperuser```

Once you've created the superuser, you can start the development server again by running: ```python manage.py runserver```

Open a web browser and go to ```http://127.0.0.1:8000/admin/```. You should see the Django admin login page.

## Django Models
Django models are Python classes that represent the structure and behavior of your application's database. They define the schema of your database tables and provide an abstraction layer for interacting with the database.

**Define a Model:** 

In your Django project, open the models.py file inside your app's directory. By default, there's a models.py file inside the myproject directory for the initial app.

Example, in models.py of your django app:
```
from django.db import models

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    pub_date = models.DateTimeField('date published')
```

**Create Migrations:** ```python manage.py makemigrations```

This command generates migration files in the migrations directory of your app. Migrations are scripts that describe how to apply changes to the database schema.

**To apply the migrations and create database tables:** ```python manage.py migrate```

**Interacting with the Database:**

To interact with the database using your model, you can use the Django manage.py shell: ```python manage.py shell```

Inside the shell, you can create and query objects based on your model. For example:
```
# Import the model
from myapp.models import BlogPost
from django.utils import timezone

# Create a new blog post
post = BlogPost(title="My First Post", content="This is the content of my first post.", pub_date=timezone.now())

# Save the post to the database
post.save()

# Query all blog posts
all_posts = BlogPost.objects.all()
```

**Admin Interface for managing models**

Django provides an admin interface that allows you to manage your application's data through a web interface. To enable it, you can create an admin class for your model in the admin.py file of your app:

```
from django.contrib import admin
from .models import BlogPost

admin.site.register(BlogPost)
```

You can then access the admin interface at ```http://127.0.0.1:8000/admin/``` and log in with the admin user credentials you created during the project setup.

## Views, Templates and URL Routing

In Django, views are responsible for processing incoming requests and returning responses. Templates are used to define the structure and presentation of the HTML pages your application generates. 

**Views**

Views in Django are implemented as **Python functions**. You can create a view function in your app's views.py file. For example, let's create a simple view to display a list of blog posts:

```
from django.shortcuts import render
from .models import BlogPost

def blog_post_list(request):
    posts = BlogPost.objects.all()
    context = {'posts': posts}
    return render(request, 'post_list.html', context)
```

In this view, we query all blog posts using the BlogPost model and pass them to the post_list.html template.

**URL Routing**

To make your view accessible via a URL, you need to define a URL pattern. Open your app's urls.py file and configure a URL route for the view. For example:

```
from django.urls import path
from .views import blog_post_list

urlpatterns = [
    path('posts/', blog_post_list, name='blog_post_list'),
]
```

This pattern maps the URL /posts/ to the blog_post_list view function.

In your project's main urls.py (e.g., "myproject/urls.py"), include the app's URL patterns using the include function:

```
from django.contrib import admin
from django.urls import path, include 

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('myapp.urls')),
]
```
This is necessary to route requests to the app's URL patterns.

**Templates**

Templates are HTML files that define the structure of your web pages. Create a new directory called templates inside your app's directory if it doesn't already exist. 

>**Django will search for templates in the app's "templates" directory by default.**


Inside the templates directory, create an HTML file for your view (e.g., post_list.html):

```
<!DOCTYPE html>
<html>
<head>
    <title>Blog Post List</title>
</head>
<body>
    <h1>Blog Post List</h1>
    <ul>
        {% for post in posts %}
            <li>{{ post.title }}</li>
        {% endfor %}
    </ul>
</body>
</html>
```

In this example, we use Django's template language to loop through the list of blog posts and display their titles.

- Template Context
  When rendering a template in Django, you provide a context, which is a dictionary containing variable names and their values. For example: ```context = {'user': current_user, 'posts': post_list}```. These variables can then be accessed in the template using the variable syntax {{ variable_name }}.

- Variables: 
  In Django templates, you can display the values of variables using double curly braces {{ }}. For example: ```<p>Welcome, {{ user.username }}!</p>```. In this example, user.username is a variable, and its value will be dynamically inserted into the HTML when the template is rendered.

- Filters:
    Django provides filters to modify the output of variables. Filters are applied using the pipe symbol |. For instance:
    ```<p>Today's date: {{ current_date|date:"F j, Y" }}</p>```. In this case, the date filter formats the current_date variable as a human-readable date.

- Tags:
  Django templates also use tags, which are enclosed in curly braces with percent signs {% %}, to perform control logic, loops, and other template-related operations. You can use tags like {% if %}, {% else %}, and {% endif %} to create conditional statements:
    ```
    {% if user.is_authenticated %}
        <p>Welcome, {{ user.username }}!</p>
    {% else %}
        <p>Please log in.</p>
    {% endif %}
    ```
    Tags like {% for %}, {% empty %}, and {% endfor %} allow you to iterate over lists or querysets:
    ```
        <ul>
        {% for post in posts %}
            <li>{{ post.title }}</li>
        {% empty %}
            <li>No posts available.</li>
        {% endfor %}
    </ul>
    ```
    You can use the {% include %} tag to include other templates within your template:
    ```<div>
        {% include "header.html" %}
    </div>
    ```

- Comments:
  You can add comments to your templates using the {# #} syntax. Comments are not rendered in the final output but can be useful for documentation or notes within your templates. ```{# This is a comment. #}```

- Template Inheritance:
  Django allows you to create a base template that defines the common structure of your site and then extend it in child templates using the {% extends %} and {% block %} tags. Child templates can override or fill in specific content areas defined in the base template.
  Base template (base.html):

    ```
    <!DOCTYPE html>
    <html>
    <head>
        <title>{% block title %}My Site{% endblock %}</title>
    </head>
    <body>
        <header>
            {% block header %}{% endblock %}
        </header>
        <main>
            {% block content %}{% endblock %}
        </main>
    </body>
    </html>
    ```

    Child template (home.html):
    ```
    {% extends "base.html" %}

    {% block title %}Home - My Site{% endblock %}

    {% block content %}
        <h1>Welcome to my website!</h1>
        <p>Content goes here...</p>
    {% endblock %}
    ```

**Rendering Templates**

In the view function, we use the render function to render the HTML template with data and return it as an HTTP response: ```return render(request, 'post_list.html', context)```

**Testing Your View**: 

Navigate to ```http://127.0.0.1:8000/posts/ ```