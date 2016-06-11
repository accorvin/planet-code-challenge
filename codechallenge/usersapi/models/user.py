from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    user_id = models.CharField(max_length=200, primary_key=True)
