from django.conf.urls import url

from . import views

app_name = 'photo'
urlpatterns = [
    url(r'^$', views.index, name='index'), 
    url(r'^allPhotos/', views.allPhotos, name='allPhotos'), 
]