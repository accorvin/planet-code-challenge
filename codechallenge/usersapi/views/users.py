import json

from django.http import HttpResponse, HttpResponseBadRequest, \
    HttpResponseNotAllowed, HttpResponseNotFound, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from usersapi.models.model_exception import ErrorType, ModelException
from usersapi.models.user import create_user, delete_user, get_user, \
    update_user, user_exists


# Generic users view. This view is hit when no userid is specified in the URL.
# This view should only be hit for a POST request when creating a user.
@csrf_exempt
def users_generic(request):
    try:
        # First check that the request is a POST request. If any other HTTP
        # method was used, return an error.
        allowed_methods = ['POST']
        if request.method not in allowed_methods:
            return HttpResponseNotAllowed(allowed_methods)
        else:
            try:
                # Get the user data from the request body. Return an error if
                # the data is malformed or missing a required key.
                try:
                    request_body = request.body.decode('utf-8')
                    request_data = json.loads(request_body)
                except Exception as e:
                    msg = 'The request body could not be parsed: {0}'
                    return HttpResponseBadRequest(msg.format(e))
                if 'userid' not in request_data:
                    msg = 'You must specify a userid'
                    return HttpResponseBadRequest(msg)
                if 'groups' not in request_data:
                    msg = "You must specify the users's groups"
                    return HttpResponseBadRequest(msg)
                user_id = request_data['userid']

                # Return an error if the specified userid already exists
                if user_exists(user_id):
                    msg = 'A user with the specified userid already exists'
                    return HttpResponseBadRequest(msg)
                else:
                    # Create the user
                    create_user(request_data)
                    return HttpResponse('User successfully created')
            except ModelException as e:
                if e.error_type is ErrorType.user:
                    return HttpResponseBadRequest(e.error_message)
                else:
                    raise
    except Exception as e:
        return HttpResponseServerError(str(e))


# Specific user view. This view gets exercised when a userid is
# specified in the request URL.
@csrf_exempt
def users_specific(request, user_id):
    try:
        # Check that the request method is allowed
        allowed_methods = ['GET', 'PUT', 'DELETE']
        if request.method not in allowed_methods:
            return HttpResponseNotAllowed(allowed_methods)
        elif request.method == 'GET':
            # If getting a user, check that the user exists
            if not user_exists(user_id):
                msg = 'A user with the specified userid does not exist'
                return HttpResponseNotFound(msg)
            else:
                user = get_user(user_id)
                return HttpResponse(user.get_output())
        elif request.method == 'DELETE':
            try:
                # Try to delete the user
                delete_user(user_id)
                return HttpResponse('User successfully deleted')
            except ModelException as e:
                # Return a 404 if the user doesn't exist
                if e.error_type is ErrorType.not_found:
                    msg = 'A user with the specified userid does not exist'
                    return HttpResponseNotFound(msg)
                else:
                    raise
        elif request.method == 'PUT':
            # First check that the specified user data is valid json
            try:
                request_body = request.body.decode('utf-8')
                request_data = json.loads(request_body)
            except ValueError:
                msg = 'The supplied user data was invalid'
                return HttpResponseBadRequest(msg)
            if user_exists(user_id):
                try:
                    # Update the user
                    update_user(user_id, request_data)
                    return HttpResponse('The user was successfully updated')
                except ModelException as e:
                    if e.error_type is ErrorType.user:
                        return HttpResponseBadRequest(e.error_message)
                    else:
                        raise
            else:
                # Return a 404 if the specified user doesn't exist
                msg = 'A user with the specified userid does not exist'
                return HttpResponseNotFound(msg)
        else:
            msg = 'The requested method is not allowed at this URl'
            return HttpResponseBadRequest(msg)
    except Exception as e:
        return HttpResponseServerError(str(e))
