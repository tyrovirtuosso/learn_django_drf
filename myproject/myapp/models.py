from django.db import models
from django.contrib.auth.models import AbstractUser

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    pub_date = models.DateTimeField('date published')
    
    class Meta:
        permissions = [
            ('can_edit_content', 'Can edit content'),
        ]

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