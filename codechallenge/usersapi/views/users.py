from django.http import HttpResponse


def users(request):
    return HttpResponse('Hello, users')
