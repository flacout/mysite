from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Picture(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    picture_name = models.CharField(max_length=255, default='NO_NAME')
    photo = models.ImageField(upload_to='pictures')
    upload_date = models.DateTimeField('date uploaded',
                                        default=timezone.localtime(timezone.now()),
                                        blank=False)

    def __str__(self):
        return self.picture_name