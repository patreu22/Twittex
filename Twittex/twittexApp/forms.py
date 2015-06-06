from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ModelForm
from .models import Posts, User, UserProfile

class newPostForm(ModelForm):
    class Meta:
        model = Posts
        fields = ['absender', 'empfaenger', 'inhalt', 'hashtags', 'mentioned']

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('desc', 'picture')