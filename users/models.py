from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLES = (
        ('user', 'User'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLES, default='user')
 
    def __str__(self):
        return '{0}, {1}, {2}, {3}, {4}, {5}, {6}'.format(
            self.id, self.username, self.password, self.first_name, self.last_name, self.email, self.role
        )
    
    
