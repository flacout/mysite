from django.conf.urls import url

from . import views

app_name = 'align'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^result/', views.result, name='result'),
    url(r'^allresults/', views.allresults, name='allresults'),
]