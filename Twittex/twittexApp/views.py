from django.shortcuts import render, redirect, RequestContext, render_to_response, Http404
from itertools import chain
from django.db.models import Q
from django.views.generic import TemplateView, CreateView, ListView, DetailView
from twittexApp.forms import UserCreationForm, AuthenticationForm, UserForm, UserProfileForm
from twittexApp.models import Posts, User, UserProfile, Nachrichten
from django.http import HttpResponse


# Create your views here.
def IndexView(request):
    if request.user.is_authenticated():
        return redirect('/home')
    else:
        return render_to_response('index.html')


def register(request):  
    # Like before, get the request's context.
    context = RequestContext(request)

    # will change when registration done
    registered = False

    # User input
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # if valid save
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            # create but dont save yet
            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # now save
            profile.save()

            # say true for template
            registered = True

        else:
            print(user_form.errors, profile_form.errors)

    # provie forms
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render_to_response(
        'register.html',
        {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
        context)


class HomeView(ListView):
    template_name = 'home.html'
    model = Posts
    success_url = '/home/'


def ProfileDetailView(request, username):
    posts = Posts.objects.all()
    user = User.objects.get(username=username)
    return render_to_response('profile.html', {'object_list': posts, 'user': user, 'request': request})


# called by submit post
def newPost(request):
    p = Posts(absender=str(request.user), inhalt=str(request.POST.get('inhalt')), hashtags='NULL', mentioned='NULL')
    p.save()
    return redirect('/home/')


#Nachrichten
class NewMsgView(ListView):
    template_name = 'newMsg.html'
    context_object_name = 'conversations'

    def get_queryset(self):
        usr = str(self.request.user)
        q = Nachrichten.objects.filter(Q(absender=usr)
                                       | Q(empfaenger=usr)).exclude(empfaenger=usr).values('empfaenger').distinct(
            'empfaenger')
        return q


def sendMsg(request):
    e = str(request.POST.get('recipient'))
    n = Nachrichten(absender=str(request.user), inhalt=str(request.POST.get('inhalt')), empfaenger=e)
    n.save()
    return redirect('/Messages/' + e)


class NachrichtenView(ListView):
    template_name = 'nachrichten.html'

    def get_queryset(self):
        usr = str(self.request.user)
        q = Nachrichten.objects.filter((Q(empfaenger=usr) & Q(absender=str(self.kwargs['author'])))
                                       | (Q(absender=usr) & Q(empfaenger=str(self.kwargs['author']))))
        return q

    def get_context_data(self, *args, **kwargs):
        context = super(NachrichtenView, self).get_context_data(*args, **kwargs)
        usr = str(self.request.user)
        context['conversations'] = Nachrichten.objects.filter(Q(absender=usr)
                                                              | Q(empfaenger=usr)).exclude(empfaenger=usr).values(
            'empfaenger').distinct('empfaenger')
        return context 
    
