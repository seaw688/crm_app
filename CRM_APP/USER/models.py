from django.db import models
from django.contrib.auth.models import AbstractUser
from CRM_APP import settings


def user_avatar_upload_path(instance, filename):
    return str(settings.MEDIA_ROOT + '/users/{0}/avatar/{1}'.format(instance.username, filename))

class User(AbstractUser):
    email = models.EmailField(unique=True)
    birth = models.DateTimeField(null=True,blank=True)
    avatar = models.ImageField(upload_to=user_avatar_upload_path,blank=True,null=True)
    position = models.CharField(max_length=30,null=True,blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]