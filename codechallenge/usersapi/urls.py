from .views.users import users_generic, users_specific
from .views.groups import groups_generic, groups_specific

from django.conf.urls import url


app_name = 'usersapi'

urlpatterns = [
    url(r'^users/?$', users_generic, name='users_generic'),
    url(r'^users/(?P<user_id>.*)/?$', users_specific,
        name='users_specific'),
    url(r'^groups/?$', groups_generic, name='groups_generic'),
    url(r'^groups/(?P<group_name>.*)/?$', groups_specific,
        name='groups_specific')
]
