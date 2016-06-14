import json


from django.http import HttpResponse, HttpResponseBadRequest, \
    HttpResponseNotAllowed, HttpResponseNotFound, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from usersapi.models.model_exception import ErrorType, ModelException
from usersapi.models.group import create_group, delete_group, get_group, \
    update_group, group_exists

@csrf_exempt
def groups_generic(request):
    try:
        allowed_methods = ['POST']
        if request.method not in allowed_methods:
            return HttpResponseNotAllowed(allowed_methods)
        else:
            try:
                request_body = request.body.decode('utf-8')
                request_data = json.loads(request_body)
                if 'name' not in request_data:
                    msg = 'You must specify a group name'
                    return HttpResponseBadRequest(msg)
                group_name = request_data['name']

                if group_exists(group_name):
                    msg = 'A group with the specified name already exists'
                    return HttpResponseBadRequest(msg)
                else:
                    create_group(group_name)
                    return HttpResponse('Group successfully created')
            except ModelException as e:
                if e.error_type is ErrorType.user:
                    return HttpResponseBadRequest(e.error_message)
                else:
                    raise
    except Exception as e:
        return HttpResponseServerError(str(e))


@csrf_exempt
def groups_specific(request, user_name):
    try:
        allowed_methods = ['GET', 'PUT', 'DELETE']
        if request.method not in allowed_methods:
            return HttpResponseNotAllowed(allowed_methods)
        elif request.method == 'GET':
            if not group_exists(group_name):
                msg = 'A group with the specified name does not exist'
                return HttpResponseNotFound(msg)
            else:
                group = get_group(group_name)
                return HttpResponse(group.get_output())
        elif request.method == 'DELETE':
            try:
                delete_group(group_name)
                return HttpResponse('Group successfully deleted')
            except ModelException as e:
                if e.error_type is ErrorType.not_found:
                    msg = 'A group with the specified name does not exist'
                    return HttpResponseNotFound(msg)
                else:
                    raise
        elif request.method == 'PUT':
            try:
                request_body = request.body.decode('utf-8')
                request_data = json.loads(request_body)
            except ValueError:
                msg = 'The supplied group data was invalid'
                return HttpResponseBadRequest(msg)
            if group_exists(group_name):
                update_group(request_data)
            else:
                msg = 'A group with the specified name does not exist'
                raise HttpResponseNotFound(msg)
        else:
            msg = 'The requested method is not allowed at this URl'
            return HttpResponseBadRequest(msg)
    except Exception as e:
        return HttpResponseServerError(e)
