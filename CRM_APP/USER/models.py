from django.db import models
from django.contrib.auth.models import AbstractUser
from CRM_APP import settings


def user_avatar_upload_path(instance, filename):
    return 'users/{0}/avatar/{1}'.format(instance.username, filename)

class User(AbstractUser):
    email = models.EmailField(unique=True)
    birth = models.DateTimeField(null=True,blank=True)
    avatar = models.ImageField(upload_to=user_avatar_upload_path,blank=True,null=True,default='/default/default.jpg')
    position = models.CharField(max_length=30,null=True,blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    def __str__(self):
        return '{0} {1}'.format(self.first_name, self.last_name)