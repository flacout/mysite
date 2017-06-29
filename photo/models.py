from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Picture(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    picture_name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='pictures')

    def __str__(self):
        return self.picture_name