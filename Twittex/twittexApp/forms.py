from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ModelForm
from .models import Posts

class newPostForm(ModelForm):
    class Meta:
        model = Posts
        fields = ['absender', 'empfaenger', 'inhalt', 'hashtags', 'mentioned']

