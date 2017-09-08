from django import forms
from django.forms import ModelForm
from .models import Picture


class UploadPhotoForm(ModelForm):
    class Meta:
        model = Picture
        exclude = ['user', 'upload_date']