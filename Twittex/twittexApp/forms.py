from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class createPostForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)
    

