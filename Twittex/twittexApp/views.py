from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from twittexApp.forms import UserCreationForm, AuthenticationForm
from twittexApp.models import User


# Create your views here.
class IndexView(TemplateView):
    template_name = 'index.html'


class RegisterView(CreateView):
    template_name = 'register.html'
    model = User
    success_url = '/'
    form_class = UserCreationForm

class HomeView(TemplateView):
    template_name = 'home.html'