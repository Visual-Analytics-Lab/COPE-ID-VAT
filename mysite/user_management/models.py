from django.contrib.auth.models import AbstractUser
from django.db import models

class my_profile_model(AbstractUser):
    title = models.CharField(max_length=32, default="", blank=True)
    department = models.CharField(max_length=64, default="", blank=True)
    organization = models.CharField(max_length=64, default="", blank=True)
    city = models.CharField(max_length=32, default="", blank=True)
    state = models.CharField(max_length=32, default='', blank=True)

    zip_code = models.CharField(max_length=5, default="", blank=True)
    country = models.CharField(max_length=32, default="", blank=True)
    favorite_projects = models.ManyToManyField('main.project_model', through='main.project_list_model', related_name='favorited_by')