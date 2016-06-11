import views

from django.conf.urls import url


app_name = 'usersapi'

urlpatterns = [
    url(r'^users.*$', views.users, name='users'),
    url(r'^group.*$', views.groups, name='groups')
]
