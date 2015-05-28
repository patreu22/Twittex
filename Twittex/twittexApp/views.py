from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, ListView
from twittexApp.forms import UserCreationForm, AuthenticationForm
from twittexApp.models import User, Posts
from django.http import HttpResponse


# Create your views here.
class IndexView(TemplateView):
    template_name = 'index.html'


class RegisterView(CreateView):
    template_name = 'register.html'
    model = User
    success_url = '/home/'
    form_class = UserCreationForm

class HomeView(ListView):
    template_name = 'home.html'
    model = Posts
    success_url ='/home/'
	
#called by submit post
def newPost(request):
    p = Posts(absender = str(request.user), inhalt = str(request.POST.get('inhalt')), empfaenger ='NULL', hashtags='NULL', mentioned='NULL')
    p.save()
    return redirect('/home/')
    #return HttpResponse(" "+str(request.user)+" "+str(request.POST.get('inhalt'))+ " ")

class createPost(CreateView):
    template_name = 'newPost.html'
    model = Posts
    fields = ['absender', 'empfaenger', 'inhalt', 'hashtags', 'mentioned']
    success_url ='/home/'

