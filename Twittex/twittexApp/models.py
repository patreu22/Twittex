from django.db import models
from django.contrib.auth.models import User

class Posts(models.Model):
    absender = models.CharField(max_length = 50)
    empfaenger = models.CharField(max_length = 50)
    inhalt = models.CharField(max_length = 140)
    hashtags = models.CharField(max_length = 100)
    mentioned = models.CharField(max_length = 140)


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    desc = models.CharField(max_length = 140, blank=True, null=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    def __unicode__(self):
        return self.user.username
    # photo = models.ImageField(upload_to='/profile_images/', default='/profile_images/no_photo.jpg')
    # followingList
    # myFollower
    # visibility(?)


class Group(models.Model):
    groupID = models.CharField(max_length = 10)
    title = models.CharField(max_length = 50)
    admin = models.CharField(max_length = 50)
    # members