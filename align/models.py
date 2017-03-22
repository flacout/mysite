from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Alignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    alignment_name= models.CharField(max_length=200)
    alignment_result = models.TextField()

    def __str__(self):
        return self.alignment_name