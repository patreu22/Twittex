from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ModelForm
from .models import Posts, User, UserProfile


class newPostForm(ModelForm):
    class Meta:
        model = Posts
        fields = ['absender', 'inhalt', 'hashtags', 'mentioned', 'datum']

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def clean(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if password and password != password2:
            raise forms.ValidationError("Passwords don't match")

        return self.cleaned_data


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('desc', 'picture')
