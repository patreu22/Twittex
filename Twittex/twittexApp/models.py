from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Posts(models.Model):
    absender = models.CharField(max_length = 50)
    inhalt = models.CharField(max_length = 140)
    hashtags = models.CharField(max_length = 100)
    mentioned = models.CharField(max_length = 140)
    datum = models.DateTimeField(default=datetime.now, blank=True)

class Nachrichten(models.Model):
    absender = models.CharField(max_length = 50)
    empfaenger = models.CharField(max_length = 50)
    inhalt = models.CharField(max_length = 140)
    datum = models.DateTimeField(default=datetime.now, blank=True)
    
