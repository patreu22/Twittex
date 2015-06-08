from django.shortcuts import render, redirect
from itertools import chain
from django.db.models import Q
from django.views.generic import TemplateView, CreateView, ListView
from twittexApp.forms import UserCreationForm, AuthenticationForm
from twittexApp.models import User, Posts, Nachrichten
from django.http import HttpResponse


# Create your views here.
class IndexView(TemplateView):
    template_name = 'index.html'


class RegisterView(CreateView):
    template_name = 'register.html'
    model = RegUser
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
    context_object_name = 'conversations'
    def get_queryset(self):
        usr = str(self.request.user)
        q = Nachrichten.objects.filter(Q(absender = usr)
                                              | Q(empfaenger = usr)).exclude(empfaenger = usr).values('empfaenger').distinct('empfaenger')
        return q

def sendMsg(request):
    e = str(request.POST.get('recipient'))
    n = Nachrichten(absender = str(request.user), inhalt = str(request.POST.get('inhalt')), empfaenger = e)
    n.save()
    return redirect('/Messages/'+e)
    
class NachrichtenView(ListView):
    template_name = 'nachrichten.html'
    
    def get_queryset(self):
        usr = str(self.request.user)
        q = Nachrichten.objects.filter((Q(empfaenger = usr) & Q(absender = str(self.kwargs['author'])))
                                        | (Q(absender = usr) & Q(empfaenger = str(self.kwargs['author']))))
        return q

    def get_context_data(self, *args, **kwargs):
        context = super(NachrichtenView, self).get_context_data(*args, **kwargs)
        usr = str(self.request.user)
        context['conversations'] = Nachrichten.objects.filter(Q(absender = usr)
                                                              | Q(empfaenger = usr)).exclude(empfaenger = usr).values('empfaenger').distinct('empfaenger')
        return context 
    
