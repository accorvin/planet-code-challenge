from django.db import models
from .group import Group
from .user import User


class GroupMember(models.Model):
    group = models.ForeignKey(Group, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
