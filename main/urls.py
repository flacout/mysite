from django.conf.urls import url

from . import views
from django.contrib.auth.views import login, logout

app_name = 'main'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^andro/$', views.android, name='android'),
    url(r'^accounts/login/$', login, name='login'),
    url(r'^accounts/logout/$', views.logout_view, name='logout'),
    url(r'^accounts/loggedin/$', views.loggedin, name='loggedin'),
    url(r'^accounts/register/$', views.register, name='register'),
    url(r'^accounts/register/complete/$', views.registration_complete, name='registration_complete'),
]