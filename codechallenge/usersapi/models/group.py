import json

from django.db import models


def get_group(group_name):
    group = Group.objects.get(group_name=group_name)
    return group


def group_exists(group_name):
    try:
        group_with_name = Group.objects.get(group_name=group_name)
        return True
    except Group.DoesNotExist:
        return False


def delete_group(group_name):
    if not group_exists(group_name):
        msg = 'A group with the name {0} does not exist'.format(group_name)
        raise ModelException(ErrorType.not_found, msg)
    else:
        group = get_group(user_id)
        group.delete()


def create_group(group_name):
    try:
        group = Group(group_name=group_name)
        group.save()
    except Exception as e:
        if group_exists(group_name):
            delete_group(group_name)
        msg = 'A server error occured. The group was not created: {0}'
        raise ModelException(ErrorType.server, msg.format(e))


def update_group(group_json):
    pass


class Group(models.Model):
    group_name = models.CharField(max_length=200, primary_key=True)

    def get_output(self):
        from .group_member import get_group_members
        users_in_group = get_group_members(self)
        output = {'userids': users_in_group}
        return json.dumps(output, indent=4)
