from django.shortcuts import render, redirect
from itertools import chain
from django.views.generic import TemplateView, CreateView, ListView
from twittexApp.forms import UserCreationForm, AuthenticationForm
from twittexApp.models import User, Posts, Nachrichten
from django.http import HttpResponse


# Create your views here.
class IndexView(TemplateView):
    template_name = 'index.html'


class RegisterView(CreateView):
    template_name = 'register.html'
    model = User
    success_url = '/login/'
    form_class = UserCreationForm

class HomeView(ListView):
    template_name = 'home.html'
    model = Posts
    success_url ='/home/'
	
#called by submit post
def newPost(request):
    p = Posts(absender = str(request.user), inhalt = str(request.POST.get('inhalt')), hashtags='NULL', mentioned='NULL')
    p.save()
    return redirect('/home/')

#Nachrichten
class NewMsgView(ListView):
    template_name = 'newMsg.html'
    def get_queryset(self):
        queryset = Nachrichten.objects.all()

def sendMsg(request):
    e = str(request.POST.get('recipient'))
    n = Nachrichten(absender = str(request.user), inhalt = str(request.POST.get('inhalt')), empfaenger = e)
    n.save()
    return redirect('/Messages/'+e)
    
class NachrichtenView(ListView):
    template_name = 'nachrichten.html'
    def get_queryset(self):
        q1 = Nachrichten.objects.filter(empfaenger = str(self.request.user))
        q2 = Nachrichten.objects.filter(absender = str(self.request.user))
        return list(chain(q2, q1))
    
