import json

from django.db import models
from .model_exception import ErrorType, ModelException
from .group import get_group, group_exists


class User(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    user_id = models.CharField(max_length=200, primary_key=True)

    def get_output(self):
        output = {}
        output['first_name'] = self.first_name
        output['last_name'] = self.last_name
        output['userid'] = self.user_id
        output['groups'] = self.get_groups_list()

        return json.dumps(output, indent=4)

    def get_groups_list(self):
        from .group_member import get_user_group_members
        groups_list = []
        group_members = get_user_group_members(self)
        for member in group_members:
            groups_list.append(member.group.group_name)
        return groups_list

    def set_groups(self, groups_list):
        from .group_member import delete_user_groups, GroupMember
        if not isinstance(groups_list, list):
            msg = 'The group data is not a valid list.'
            raise ModelException(ErrorType.user, msg)
        else:
            try:
                delete_user_groups(self)
                for group_name in groups_list:
                    if not group_exists(group_name):
                        msg = 'A group with the name {0} does not exist'
                        raise ModelException(ErrorType.not_found,
                                             msg.format(group_name))
                    else:
                        group = get_group(group_name)
                        group_member = GroupMember(group=group, user=self)
                        group_member.save()
            except ModelException:
                raise
            except Exception as e:
                delete_user_groups(self)
                msg = 'Server error! Group member not created. {0}'
                raise ModelException(ErrorType.server, msg.format(e))


def get_user(user_id):
    user = User.objects.get(user_id=user_id)
    return user


def user_exists(user_id):
    try:
        user_with_id = User.objects.get(user_id=user_id)
        return True
    except User.DoesNotExist:
        return False


def delete_user(user_id):
    from .group_member import delete_user_groups, GroupMember
    if not user_exists(user_id):
        msg = 'A user with the ID {0} does not exist'.format(user_id)
        raise ModelException(ErrorType.not_found, msg)
    else:
        user = get_user(user_id)
        delete_user_groups(user)
        user.delete()


def create_user(user_json):
    try:
        first_name = user_json['first_name']
        last_name = user_json['last_name']
        user_id = user_json['userid']
        user_groups = user_json['groups']
    except KeyError as e:
        msg = 'The required field "{0}" was not specified'.format(e)
        raise ModelException(ErrorType.user, msg)

    try:
        user = User(first_name=first_name, last_name=last_name,
                user_id=user_id)
        user.save()
        user.set_groups(user_groups)
    except Exception as e:
        if user_exists(user_id):
            delete_user(user_id)
        msg = 'A server error occured. The user was not created: {0}'
        raise ModelException(ErrorType.server, msg.format(e))


def update_user(old_user_id, user_json):
    try:
        first_name = user_json['first_name']
        last_name = user_json['last_name']
        new_user_id = user_json['userid']
        user_groups = user_json['groups']
    except KeyError as e:
        msg = 'The required field "{0}" was not specified'.format(e)
        raise ModelException(ErrorType.user, msg)

    try:
        if user_exists(old_user_id):
            user = get_user(old_user_id)
            user.user_id = new_user_id
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            user.set_groups(user_groups)
        else:
            msg = 'A user with the specified userid does not exist'
            raise HttpResponseNotFound(msg)
    except Exception as e:
        msg = 'A server error occured. The user was not updated: {0}'
        raise ModelException(ErrorType.server, msg.format(e))
