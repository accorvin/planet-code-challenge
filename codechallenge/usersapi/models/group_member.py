from django.db import models
from .group import Group
from .user import User


def get_user_group_members(user):
    try:
        user_group_members = GroupMember.objects.filter(user=user)
        return user_group_members
    except GroupMember.DoesNotExist:
        return []


def get_group_members(group):
    try:
        user_ids = []
        group_members = GroupMember.objects.filter(group=group)
        for member in group_members:
            user_ids.append(member.user.user_id)
        return user_ids
    except GroupMember.DoesNotExist:
        return []


def delete_user_groups(user):
    user_group_members = get_user_group_members(user)
    for group_member in user_group_members:
        group_member.delete()


class GroupMember(models.Model):
    group = models.ForeignKey(Group, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
