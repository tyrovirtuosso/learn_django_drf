from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    pub_date = models.DateTimeField('date published')
    
    class Meta:
        permissions = [
            ('can_edit_content', 'Can edit content'),
        ]
        
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.CharField(max_length=100)
    published_date = models.DateTimeField(auto_now_add=True)

    # The reverse() function in Django is used to dynamically generate URLs for views based on their URL patterns and the view name.
    def get_absolute_url(self):
        return reverse('post-detail', args=[str(self.id)])

class CustomUser(AbstractUser):
    # Add custom fields here
    email = models.EmailField(unique=True)
    
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