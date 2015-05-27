from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from twittexApp.forms import UserCreationForm, AuthenticationForm
from twittexApp.models import User, Posts


# Create your views here.
class IndexView(TemplateView):
    template_name = 'index.html'


class RegisterView(CreateView):
    template_name = 'register.html'
    model = User
    success_url = '/home/'
    form_class = UserCreationForm

class HomeView(TemplateView):
    template_name = 'base.html'

class createPost(CreateView):
    template_name = 'newPost.html'
    model = Posts
    fields = ['absender', 'empfaenger', 'inhalt', 'hashtags', 'mentioned']
    success_url ='/home/'
