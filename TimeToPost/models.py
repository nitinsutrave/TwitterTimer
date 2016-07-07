from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Users(models.Model):
    user_name = models.CharField(max_length=60)
    user_id = models.CharField(max_length=60)
    user_access_token = models.CharField(max_length=150)
    user_access_secret = models.CharField(max_length=150)
