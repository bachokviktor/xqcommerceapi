from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField


class CustomUser(AbstractUser):
    """
    Custom user model.
    """
    profile_pic = models.ImageField(upload_to="profile_pic/", blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    country = CountryField(blank=True, null=True)

    def __str__(self):
        return self.username
