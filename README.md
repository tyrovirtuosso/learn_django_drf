## Table of Contents

- [Table of Contents](#table-of-contents)
- [Learn Django and Django Rest Framework](#learn-django-and-django-rest-framework)
- [Set up your Django development environment](#set-up-your-django-development-environment)
- [Django Models](#django-models)
- [Views, Templates and URL Routing](#views-templates-and-url-routing)
- [Handling Forms in Django](#handling-forms-in-django)
- [User Authentication](#user-authentication)
- [User Authorization](#user-authorization)
- [Common Class-Based Views(CBV)](#common-class-based-viewscbv)


## Learn Django and Django Rest Framework

This repository is a learning resource for getting familiar with Django and Django Rest Framework (DRF).

**Intro**

Django, an open-source web framework for building web applications using Python, the MVC (Model-View-Controller)  architecture is implemented slightly differently and is often referred to as the MTV (Model-Template-View) pattern.

- Model (M - Model):

Model defines the structure of your database tables and how data is stored, retrieved, and manipulated.
Django uses Object-Relational Mapping (ORM) to map Python objects to database tables. This means you define your data models in Python classes, and Django handles the database interactions for you.

- Template (T - Template):

The Template in Django is similar to the View in the traditional MVC pattern. It is responsible for handling the presentation logic and rendering the HTML that is sent to the user's web browser.
Templates in Django are essentially HTML files with placeholders for dynamic content. 

- View (V - View):

In Django, the View is responsible for processing user requests, interacting with the Model to retrieve or manipulate data, and then passing the data to the Template for rendering.
Views in Django are implemented as Python functions or classes. They receive incoming HTTP requests, perform any necessary data processing or business logic, and return an HTTP response, often by rendering a Template with the data.

- Serialization

In Django, serialization refers to the process of converting complex data types, such as Django QuerySets or model instances, into a format that can be easily rendered into JSON, XML, or other content types. The purpose of serialization is to make it easy to transmit data between your Django application and other systems or clients, particularly over HTTP in RESTful APIs.

- QuerySet

In Django, a queryset is a powerful and flexible way to retrieve data from your database. It represents a collection of database queries that can be used to filter and manipulate data before it's fetched from the database.

Key characteristics of a queryset include:

1. Lazy Evaluation: Querysets are lazily evaluated, which means they are not executed against the database until you explicitly evaluate them. This allows you to chain multiple filters and transformations together before retrieving the data, which can be more efficient.
2. Filtering and Filtering Methods: You can use filtering methods like .filter(), .exclude(), and .get() to narrow down the results based on certain conditions, such as field values or relationships. 
   
```
# Retrieve all posts published by a specific author
queryset = Post.objects.filter(author="John Doe")
```
   
3. Chaining: Querysets can be chained together to create more complex queries. This is useful for combining multiple filters and conditions.
   
```
# Retrieve all published posts by John Doe with "Django" in the title
queryset = Post.objects.filter(author="John Doe").filter(title__icontains="Django")
``` 

4. Slicing and Pagination: You can use slicing to retrieve a subset of results, which is handy for implementing pagination.

```
# Retrieve the first 10 posts
queryset = Post.objects.all()[:10]
```

## Set up your Django development environment 
This repo will be used to famillirize myself with Django and Django Rest Framework(DRF)

**Package Installation:** ```pip install Django python-dotenv```

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

**Django will search for templates in the app's "templates" directory by default.**


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

## Handling Forms in Django

In Django, forms are represented by Python classes that inherit from django.forms.Form. In your "myapp" directory, create a Python file named forms.py if it doesn't exist already. 

```
# myapp/forms.py
from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
```

**Render the Form in a Template**

Create an HTML template (e.g., contact.html) inside the "templates" directory

```
<!-- templates/contact.html -->
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Submit</button>
</form>

{% if form.errors %}
    <div class="alert alert-danger">
        <strong>Error:</strong> Please correct the errors below.
    </div>
{% endif %}
```

{{ form.as_p }} is a template tag in Django's template language that is used to render a form as a series of paragraphs in an HTML form element. It's a convenient way to generate the HTML for each form field, with each field wrapped in a <p> (paragraph) HTML tag.

CSRF (Cross-Site Request Forgery) is a security vulnerability that occurs when an attacker tricks a user into unknowingly making an unwanted request to a different website. To protect against CSRF attacks, Django includes a built-in mechanism called the CSRF token.

A CSRF token is a random, unique value associated with a user's session. This token is added to forms in Django to verify that the form submission is legitimate and originated from the same website, rather than being a malicious request from a different source.

Here's how the CSRF token works in Django:

- Generation: When a user visits a Django site, a unique CSRF token is generated and associated with their session. This token is usually stored in a cookie or in the user's session data on the server.
- Inclusion in Forms: Whenever Django renders a form in a template, it automatically includes the CSRF token as a hidden field within the form. 
- Submission: When the user submits the form, the browser includes the CSRF token as part of the POST data sent to the server.
- Validation: On the server side, Django checks that the received CSRF token matches the one associated with the user's session. If they match, it indicates that the form submission is legitimate and not a CSRF attack.

**Handle Form Submissions in a View**

In your "myapp/views.py" file, create a view function to handle the form submission and rendering:

```
# myapp/views.py
from django.shortcuts import render, redirect
from .forms import ContactForm


def success_page(request):
    return render(request, 'success.html')

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the form data (e.g., send an email)
            return redirect('success_page')  # Redirect to a success page
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})
```

This view function handles both GET (initial form display) and POST (form submission) requests. If the form is valid, it can take action (e.g., send an email) and redirect to a success page.

The redirect('success_page') is a Django function that is used to perform a redirect to a specific URL or view name after a successful form submission or any other action that requires a redirect in your web application.

```success.html``` template:

```
<!DOCTYPE html>
<html>
<head>
    <title>Form Submission Success</title>
</head>
<body>
    <h1>Thank You!</h1>
    <p>Your form submission was successful.</p>
    <p>We appreciate your feedback.</p>
</body>
</html>
```

Don't forget to add success_page view url in your apps urls.py:

```
urlpatterns = [
    # Other URL patterns
    path('success/', views.success_page, name='success_page'),
]
```

**Setting Up a URL Route for the Form View**

In your "myapp/urls.py" file, you need to define a URL pattern that maps to the view function responsible for handling the form

```
from django.urls import path
from . import views

urlpatterns = [
    path('contact/', views.contact_view, name='contact_view'),
]
```

## User Authentication 

Django includes a built-in User model for handling user accounts. You can use the default User model or create a custom user model to extend it with additional fields. In your myapp/models.py file:

**Default:** ```from django.contrib.auth.models import User```

**Custom:** 

```
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # Add custom fields here
    age = models.PositiveIntegerField(null=True, blank=True)
```

- When creating custom user models, make sure you add 'related_name' argument to your custom fields to avoid a clash in reverse accessor names between the default Django User model and your custom CustomUser model. By default, Django generates reverse accessors with the same names. You're dealing with the groups and user_permissions fields in a custom user model (CustomUser) that extends Django's built-in User model.


- ```related_name='custom_user_set':``` This line specifies a custom name for the reverse relation from auth.Group (Django's built-in group model) to the CustomUser model. Instead of using the default reverse relation name, which would be user_set, it's changed to custom_user_set.

```
# myapp/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Add custom fields here
    age = models.PositiveIntegerField(null=True, blank=True)
    
    # Add related_name to avoid clashes with the default User model
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
        error_messages={
            'unique': 'This user permission already exists.',
        },
    )
```

- Custom User Creation Form: You should create a custom user creation form (usually in forms.py) that includes the age field along with other fields like username, email, and password

```
from django import forms
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')
```

- View Logic: In your registration view or user creation logic, you would use this custom form to handle user input, including the age field. Here's a simplified example of a registration view that uses the form:

```
from .forms import CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.email = form.cleaned_data['email']
            user.save()
            
            # Get or create the 'All Users' group
            group, created = Group.objects.get_or_create(name='All Users')

            # Add the user to the 'All Users' group
            user.groups.add(group)
            
            login(request, user)  # Log the user in
            return redirect('profile')  # Redirect to user's profile
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
```

- Ensure your AUTH_USER_MODEL setting is correctly configured: In your project's settings (usually settings.py), make sure you have configured the AUTH_USER_MODEL setting to point to your custom user model: ```AUTH_USER_MODEL = 'myapp.CustomUser'```

**User Registration**

Create a registration view in myapp/views.py to handle user registration. Use Django's built-in UserCreationForm for simplicity:

```
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


@login_required
def profile(request):
    return render(request, 'profile.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in
            return render(request, 'accounts/profile.html')  # Redirect to user's profile by using the 'profile' view or url
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
```

create **"register.html"** in "myapp/templates/registration/"

```
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Register</button>
</form>
```

Create the Profile Template in myapp/templates/accounts/profile.html(by default django checks the 'accounts' directory in templates). You can override this by placing ```LOGIN_REDIRECT_URL = '/profile/'``` in settings.py. Make sure that the path you specify (/profile/) matches the URL pattern for your profile view.

```
<!DOCTYPE html>
<html>
<head>
    <title>User Profile</title>
</head>
<body>
    <h1>Welcome to Your Profile Page</h1>
    <!-- Display user-specific content or information here -->
</body>
</html>
```

Add the url: ```path('profile/', views.profile, name='profile'),```

**Login and Logout**

Django provides built-in views and templates for user login and logout. Customize them as needed:

**Login:**

```
from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
```

- Add the url path: ```path('login/', views.CustomLoginView.as_view(), name='login'),```
- Create template in templates/registration/login.html
  
```
  <!-- myapp/templates/registration/login.html -->
{% extends "base.html" %}

{% block content %}
  <h2>Login</h2>
  <form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Login</button>
  </form>
{% endblock %}
```

- Here's the **base.html** in templates/

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}My Website{% endblock %}</title>
</head>
<body>
    <header>
        <!-- Header content goes here -->
        <h1>My Website</h1>
        <nav>
            <!-- Navigation menu goes here -->
            <ul>
                <li><a href="/">Home</a></li>
                <li><a href="{% url 'login' %}">Login</a></li>
                <li><a href="{% url 'logout' %}">Logout</a></li>
            </ul>
        </nav>
    </header>
    <main>
        <!-- Main content goes here -->
        {% block content %}{% endblock %}
    </main>
    <footer>
        <!-- Footer content goes here -->
        <p>&copy; 2023 My Website</p>
    </footer>
</body>
</html>
```

 The {% block %} template tags define areas where child templates can override or extend the content.

- Add Login URL to Navigation

In your navigation menu or any relevant place in your templates, you can add a link to the login page: ```<a href="{% url 'login' %}">Login</a>```

- Add logout navigation: ```<a href="{% url 'logout' %}">Logout</a>s```


**Logout:**

```
from django.contrib.auth.views import LogoutView

class CustomLogoutView(LogoutView):
    next_page = 'login'  # Redirect to the login page after logout
```

- Define a Logout URL Pattern

```path('logout/', views.CustomLogoutView.as_view(), name='logout'),  # Map the URL to the logout view```

## User Authorization

Django includes a permissions system that allows you to assign specific permissions to users and groups.

**User Permissions**

- Define user permissions in myapp/models.py and apply them in your views. Here's an example:

```
# myapp/models.py
class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    pub_date = models.DateTimeField('date published')
    
    class Meta:
        permissions = [
            ('can_edit_content', 'Can edit content'),
        ]
```


- After defining this custom permission in the BlogPost model's Meta class, you can use it to control access to specific views or operations related to BlogPost objects. For example, you can use the @permission_required decorator to restrict access to views that allow editing BlogPost content:
  
```
# myapp/views.py
from django.contrib.auth.decorators import permission_required

@permission_required('myapp.can_edit_content')
def edit_view(request):
    # View logic here
```

- Permission Name (can_edit_content):
  - can_edit_content is the name of the custom permission you're defining. This name is used to identify the permission.
- Permission Description (Can edit content):
  - This is a human-readable description of the permission. It provides a brief explanation of what the permission allows. In this case, it suggests that users with this permission can edit content.

In this example, the @permission_required decorator checks if the user has the "can_edit_content" permission (myapp.can_edit_content). If the user has the permission, they can access the edit_blog_post view.

You can also use permissions in the Django admin panel to control who can edit BlogPost objects.

- Checking Permissions in Views:

```
if request.user.has_perm('myapp.can_edit_content'):
    # Allow access to content editing features
```

- To handle cases where a user doesn't have permission to access a view and display a "You're not allowed" page, you can use Django's @permission_required decorator in conjunction with a custom template for unauthorized access:

create a custom template (e.g., unauthorized.html) that displays a message indicating that the user is not allowed to access the page:

```
<!DOCTYPE html>
<html>
<head>
    <title>Unauthorized</title>
</head>
<body>
    <h1>You're not allowed to access this page.</h1>
    <!-- You can provide additional information or links here -->
</body>
</html>
```

- Specify a login_url parameter in the view to redirect users to the "Unauthorized" page if they don't have the required permission: ```@permission_required('myapp.can_edit_content', login_url='/unauthorized/')```

- Map the url: ````path('unauthorized/', views.unauthorized_page, name='unauthorized_page'),```

- Create the "Unauthorized" View: ```def unauthorized_page(request): return render(request, 'unauthorized.html')```

**Middleware for Permissions**
Django's authentication middleware checks permissions for each request automatically. You can use decorators like @login_required to restrict access to views.

 **Groups**
 You can organize users into groups and assign permissions to groups rather than individual users. 
 
 Example: Creating a Group and Assigning Permissions:

```
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

# Create a group
group = Group.objects.create(name='Content Editors')

# Assign permissions to the group
content_type = ContentType.objects.get_for_model(MyModel)
permission = Permission.objects.get(content_type=content_type, codename='can_edit_content')
group.permissions.add(permission)

# Add users to the group
user.groups.add(group)
```

- Heres an example of adding users to a group after registration:

```
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.email = form.cleaned_data['email']
            user.save()
            
            # Get or create the 'All Users' group
            group, created = Group.objects.get_or_create(name='All Users')
            
            # Get the content type for the BlogPost model
            content_type = ContentType.objects.get_for_model(BlogPost)
            
            # Add permission to group            
            permission = Permission.objects.get(content_type=content_type, codename='can_edit_content')
            group.permissions.add(permission)

            # Add the user to the 'All Users' group
            user.groups.add(group)
            
            login(request, user)  # Log the user in
            return redirect('profile')  # Redirect to user's profile
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
```

**ContentType**

In Django, the ContentType model is a built-in model provided by the Django contenttypes framework. It is used to represent and manage the types of content or models that exist in your Django project. The ContentType model is particularly useful for scenarios where you need to create relationships or associations between different models in a flexible way, often seen in applications that involve permissions, content tagging, or generic relations.

Here's what ContentType means and how it's typically used:

- Representation of Model Types:

    ContentType represents the types or classes of Django models in your project. Each ContentType instance corresponds to a specific Django model. It holds information about the app label and the model name.

- Use Cases:

    Permissions: In Django's permission system, ContentType is used to associate permissions with specific models. It allows you to specify which users or groups have permissions to perform certain actions on particular models.

    Generic Relations: When you want to create a model that can be related to various other models without explicitly defining foreign keys for each relationship, you can use GenericForeignKey. ContentType is used in conjunction with GenericForeignKey to create generic relationships.

    Content Tagging: If you want to create a tagging system where multiple models can be tagged with different categories or keywords, you can use ContentType to track the types of content that can be tagged.


## Common Class-Based Views(CBV)

- DetailView: Displaying details of a single object.
- ListView: Displaying a list of objects.
- CreateView: Creating new objects.
- UpdateView: Updating existing objects.
- DeleteView: Deleting objects.

For demonstration, lets Define the Model:

- Define Model

```
# blog/models.py
from django.db import models
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.CharField(max_length=100)
    published_date = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('post-detail', args=[str(self.id)])
```

The reverse() function is a convention in Django, used to dynamically generate URLs for views based on their URL patterns and the view name. So, when you call reverse('post-detail', args=[str(self.id)]), it dynamically generates a URL for the detail view of the current Post instance, incorporating the primary key of that instance into the URL. This allows you to easily link to the detail page for any Post object without hardcoding the URLs, making your code more maintainable and flexible.

- Create Views

```
# blog/views.py
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView,
)
from .models import Post

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
```

LoginRequiredMixin and the @login_required decorator serve a similar purpose: they both restrict access to views to authenticated users. 

LoginRequiredMixin is used as a class-based mixin in Django's class-based views (CBVs) while @login_required is a decorator that you apply to function-based views (FBVs).

We import reverse_lazy instead of reverse because it's recommended to use reverse_lazy for class-based views, especially in attributes like success_url.

Also keep the below in mind if url path isn't working:


In Settings: 
```
LOGIN_REDIRECT_URL = '/profile/'
LOGIN_URL = '/custom-login/'  # Change this to your desired login URL
```

LOGIN_URL: This setting specifies the URL where unauthenticated users are redirected when they try to access a view that requires authentication. It acts as the login page URL. By default, it is set to /accounts/login/.

LOGIN_REDIRECT_URL: This setting specifies the URL where users are redirected to after a successful login. It determines where the user is taken after they log in. For example, after a user successfully logs in, they will be redirected to the URL specified in LOGIN_REDIRECT_URL. You can customize this URL to control where users are taken after logging in.


- Define URLs

```
# blog/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('post/create/', views.PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('posts/', views.PostListView.as_view(), name='post-list'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
]
```

- Create HTML Templates

```blog/templates/blog/post_form.html (for PostCreateView and PostUpdateView):```

```
{% extends 'base.html' %}

{% block content %}
  <h2>{% if request.resolver_match.url_name == 'post-create' %}Create{% else %}Update{% endif %} Post</h2>
  <form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Save</button>
  </form>
{% endblock %}
```

```blog/templates/blog/post_detail.html (for PostDetailView):```

```
{% extends 'base.html' %}

{% block content %}
  <h2>{{ post.title }}</h2>
  <p>Author: {{ post.author }}</p>
  <p>Published Date: {{ post.published_date }}</p>
  <p>{{ post.content }}</p>
  <a href="{% url 'post-update' post.pk %}">Edit</a>
  <a href="{% url 'post-delete' post.pk %}">Delete</a>
{% endblock %}
```

```blog/templates/blog/post_list.html (for PostListView):```

```
{% extends 'base.html' %}

{% block content %}
  <h2>Blog Posts</h2>
  <ul>
    {% for post in posts %}
      <li><a href="{% url 'post-detail' post.pk %}">{{ post.title }}</a></li>
    {% empty %}
      <li>No posts yet.</li>
    {% endfor %}
  </ul>
  <a href="{% url 'post-create' %}">Create New Post</a>
{% endblock %}
```

```blog/templates/blog/post_confirm_delete.html (for PostDeleteView):```

```
{% extends 'base.html' %}

{% block content %}
  <h2>Confirm Deletion</h2>
  <p>Are you sure you want to delete "{{ post.title }}"?</p>
  <form method="post">
    {% csrf_token %}
    <button type="submit">Delete</button>
    <a href="{% url 'post-detail' post.pk %}">Cancel</a>
  </form>
{% endblock %}
```