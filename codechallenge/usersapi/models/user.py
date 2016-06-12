import json

from django.db import models
from .model_exception import ErrorType, ModelException


class User(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    user_id = models.CharField(max_length=200, primary_key=True)

    def get_output(self):
        output = {}
        output['first_name'] = self.first_name
        output['last_name'] = self.last_name
        output['userid'] = self.user_id

        return json.dumps(output, indent=4)


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
    if not user_exists(user_id):
        msg = 'A user with the ID {0} does not exist'.format(user_id)
        raise ModelException(ErrorType.not_found, msg)
    else:
        user = get_user(user_id)
        user.delete()


def create_user(user_json):
    try:
        first_name = user_json['first_name']
        last_name = user_json['last_name']
        user_id = user_json['userid']
    except KeyError as e:
        msg = 'The required field "{0}" was not specified'.format(e)
        raise ModelException(ErrorType.user, msg)

    try:
        user = User(first_name=first_name, last_name=last_name,
                user_id=user_id)
        user.save()
    except Exception as e:
        if user_exists(user_id):
            delete_user(user_id)
        msg = 'A server error occured. The user was not created: {0}'
        raise ModelException(ErrorType.server, msg.format(e))


def update_user(user_json):
    pass
