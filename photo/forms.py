from django import forms
from django.forms import ModelForm
from .models import Picture

'''
class UploadPhotoForm(forms.Form):
    topic = forms.CharField()
    picture = forms.ImageField()
'''

class UploadPhotoForm(ModelForm):
    class Meta:
        model = Picture
        fields = ['picture_name', 'photo']