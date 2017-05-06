from django.conf.urls import url

from . import views

app_name = 'align'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^result/', views.result, name='result'),
    url(r'^allresults/(?P<page_nb>[1-9]+)/', views.accountResults, name='allresultsPages'),
    url(r'^allresults/', views.accountResults, name='allresults'),
    
]