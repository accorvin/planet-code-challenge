from django.db import models


class Group(models.Model):
    group_name = models.CharField(max_length=200, primary_key=True)
