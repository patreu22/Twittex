from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, ListView
from twittexApp.forms import UserCreationForm, AuthenticationForm
from twittexApp.models import User, Posts
from django.http import HttpResponse
import smtplib


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
    p = Posts(absender = str(request.user), inhalt = str(request.POST.get('inhalt')), empfaenger ='NULL', hashtags='NULL', mentioned='NULL')
    p.save()
    return redirect('/home/')

def contact(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        # A POST request: Handle Form Upload
        form = ContactForm(request.POST)
 
        # If data is valid, proceeds to create a new post and redirect the user
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            SERVER = "localhost"

            FROM = email
            TO = ["Twittex@yahoo.com"]

            SUBJECT = "Mail from" + name

            TEXT = message

            # Prepare actual message

            mail = """\
            From: %s
            To: %s
            Subject: %s

            %s
            """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

            # Send the mail

            server = smtplib.SMTP(SERVER)
            server.sendmail(FROM, TO, mail)
            server.quit()
