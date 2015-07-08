from django.db import models
from django.contrib.auth.models import User
from django import forms
from datetime import datetime


class Posts(models.Model):
    Post_Privacy_CHOICES = (
    ('Pub', 'Public'),
    ('OF', 'only Followers'),
    ('OM', 'only Me'),
)
    inhalt = models.CharField(max_length=140)
    hashtags = models.CharField(max_length=100)
    datum = models.DateTimeField(default=datetime.now, blank=True)
    autor = models.ForeignKey(User)
    mentioned = models.ManyToManyField(User, related_name='mentioned')
    privacy= models.CharField(max_length = 3,choices=Post_Privacy_CHOICES,default='Pub')


class Conversation(models.Model):
    absender = models.ForeignKey(User, related_name='absender')
    empfaenger = models.ForeignKey(User)
    inhalt = models.CharField(max_length=140)
    datum = models.DateTimeField(default=datetime.now, blank=True)

class EmailForm(forms.Form):
    name = forms.CharField(max_length=255)
    email = forms.EmailField()
    subject = forms.CharField(max_length=255)
    message = forms.CharField()


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    desc = models.CharField(max_length = 140, blank=True, null=True)
    picture = models.ImageField(upload_to='profile_pictures', blank=True, default='no_photo.jpg')
    mentioned_count = models.IntegerField(default=0)
    follows = models.ManyToManyField('UserProfile', related_name='followed_by')
    privacy = models.BooleanField(default=False)
    # false fuer alle sichtbar
    # true nur fuer die ich folge sichbar

    def __unicode__(self):
        return self.user.username

    def getPicture(self):
        if not self.picture:
            return '/media/no_photo.jpg'
        else:
            return self.picture.url


class List(models.Model):
    title = models.CharField(max_length = 25)
    admin = models.ForeignKey(User)
    userlist = models.ManyToManyField(User, related_name='userlist', blank=True)
