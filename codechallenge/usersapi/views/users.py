import json

from django.http import HttpResponse, HttpResponseBadRequest, \
    HttpResponseNotAllowed, HttpResponseNotFound, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from usersapi.models.model_exception import ErrorType, ModelException
from usersapi.models.user import create_user, delete_user, get_user, \
    update_user, user_exists


@csrf_exempt
def users_generic(request):
    try:
        allowed_methods = ['POST']
        if request.method not in allowed_methods:
            return HttpResponseNotAllowed(allowed_methods)
        else:
            try:
                request_body = request.body.decode('utf-8')
                request_data = json.loads(request_body)
                if 'userid' not in request_data:
                    msg = 'You must specify a userid'
                    return HttpResponseBadRequest(msg)
                if 'groups' not in request_data:
                    msg = "You must specify the users's groups"
                    return HttpResponseBadRequest(msg)
                user_id = request_data['userid']

                if user_exists(user_id):
                    msg = 'A user with the specified userid already exists'
                    return HttpResponseBadRequest(msg)
                else:
                    create_user(request_data)
                    return HttpResponse('User successfully created')
            except ModelException as e:
                if e.error_type is ErrorType.user:
                    return HttpResponseBadRequest(e.error_message)
                else:
                    raise
    except Exception as e:
        return HttpResponseServerError(str(e))


@csrf_exempt
def users_specific(request, user_id):
    try:
        allowed_methods = ['GET', 'PUT', 'DELETE']
        if request.method not in allowed_methods:
            return HttpResponseNotAllowed(allowed_methods)
        elif request.method == 'GET':
            if not user_exists(user_id):
                msg = 'A user with the specified userid does not exist'
                return HttpResponseNotFound(msg)
            else:
                user = get_user(user_id)
                return HttpResponse(user.get_output())
        elif request.method == 'DELETE':
            try:
                delete_user(user_id)
                return HttpResponse('User successfully deleted')
            except ModelException as e:
                if e.error_type is ErrorType.not_found:
                    msg = 'A user with the specified userid does not exist'
                    return HttpResponseNotFound(msg)
                else:
                    raise
        elif request.method == 'PUT':
            try:
                request_body = request.body.decode('utf-8')
                request_data = json.loads(request_body)
            except ValueError:
                msg = 'The supplied user data was invalid'
                return HttpResponseBadRequest(msg)
            if user_exists(user_id):
                update_user(old_user_id, request_data)
            else:
                msg = 'A user with the specified userid does not exist'
                raise HttpResponseNotFound(msg)
        else:
            msg = 'The requested method is not allowed at this URl'
            return HttpResponseBadRequest(msg)
    except Exception as e:
        return HttpResponseServerError(e)
