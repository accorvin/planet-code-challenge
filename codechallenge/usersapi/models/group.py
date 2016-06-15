import json

from django.db import models
from .model_exception import ErrorType, ModelException
from .user import get_user, user_exists


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
        group = get_group(group_name)
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


def update_group(group_name, group_members):
    try:
        if group_exists(group_name):
            group = get_group(group_name)
            group.reset_members(group_members)
        else:
            msg = 'A group with the specified name does not exist'
            raise ModelException(ErrorType.user, msg)
    except ModelException:
        raise
    except Exception as e:
        msg = 'A server error occured. The group was not updated: {0}'
        raise ModelException(ErrorType.server, msg.format(e))


class Group(models.Model):
    group_name = models.CharField(max_length=200, primary_key=True)

    def get_output(self):
        from .group_member import get_group_members
        members_in_group = get_group_members(self)
        users_in_group = []
        for member in members_in_group:
            users_in_group.append(member.user.user_id)
        output = {'userids': users_in_group}
        return json.dumps(output, indent=4)

    def delete_members(self):
        from .group_member import delete_group_users, GroupMember
        delete_group_users(self)

    def reset_members(self, members):
        from .group_member import GroupMember
        for user_id in members:
            if not user_exists(user_id):
                msg = 'The specified user {0} does not exist'.format(user_id)
                raise ModelException(ErrorType.user, msg)
        self.delete_members()
        for user_id in members:
            user = get_user(user_id)
            group_member = GroupMember(group=self, user=user)
            group_member.save()

