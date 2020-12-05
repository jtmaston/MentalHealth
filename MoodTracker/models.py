from django.db import models
from django.contrib.auth.models import User
from fernet_fields import EncryptedTextField


class Entry(models.Model):
    date_added = models.DateTimeField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    mood = models.IntegerField()
    activity = models.CharField(max_length=300)
    note = EncryptedTextField()
