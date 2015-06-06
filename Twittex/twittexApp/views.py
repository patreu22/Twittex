from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, ListView, DetailView
from twittexApp.forms import UserCreationForm, AuthenticationForm
from twittexApp.models import Posts, User, UserProfile
from django.http import HttpResponse


# Create your views here.
class IndexView(TemplateView):
    template_name = 'index.html'


class RegisterView(CreateView):
    template_name = 'register.html'
    model = UserProfile
    success_url = '/login/'
    form_class = UserCreationForm

class HomeView(ListView):
    template_name = 'home.html'
    model = Posts
    success_url ='/home/'

class ProfileView(TemplateView):
    template_name = 'profile.html'
    success_url ='/profile/'
	
#called by submit post
def newPost(request):
    p = Posts(absender = str(request.user), inhalt = str(request.POST.get('inhalt')), empfaenger ='NULL', hashtags='NULL', mentioned='NULL')
    p.save()
    return redirect('/home/')
