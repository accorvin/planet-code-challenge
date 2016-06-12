from .views.users import users_generic, users_specific
from .views.groups import groups

from django.conf.urls import url


app_name = 'usersapi'

urlpatterns = [
    url(r'^users/?$', users_generic, name='users_generic'),
    url(r'^users/(?P<user_id>.*)/?$', users_specific,
        name='users_specific'),
    url(r'^groups/?$', groups, name='groups')
]
