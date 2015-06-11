from django.shortcuts import render, redirect, RequestContext, render_to_response, Http404
from itertools import chain
from django.db.models import Q
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView
from twittexApp.forms import UserCreationForm, AuthenticationForm, UserForm, UserProfileForm, PostsName
from twittexApp.models import Posts, User, UserProfile, Nachrichten, EmailForm, models
from django.http import HttpResponse
import smtplib
from django.core.mail import send_mail

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


class ProfileEditView(UpdateView):
    template_name = 'editprofile.html'
    success_url = '/'
    fields = ['desc', 'picture']

    def get_object(self):
        return UserProfile.objects.get(user=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        # check if there is some video onsite
        if self.kwargs['username'] != request.user.username:
            return redirect('/')
        else:
            return super(ProfileEditView, self).dispatch(request, *args, **kwargs)


# called by submit post
def newPost(request):
    content = str(request.POST.get('inhalt'))
    #hashtag search from http://stackoverflow.com/questions/6331497
    hashtags = {tag.strip("#") for tag in content.split() if tag.startswith("#")}
    mentioned = {tag.strip("@") for tag in content.split() if tag.startswith("@")}
    p = Posts(absender=str(request.user), inhalt=content, hashtags=str(hashtags), mentioned=str(mentioned))
    p.save()
    return redirect('/home/')

def sendmail(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            content = name + " " + "<" + email + ">" + " send the following message: \n \n " + message
            send_mail(subject, content, email, ['twittexsn@gmail.com'])
            return redirect('/thanks/')
        else:
            return redirect('/contact/')

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
    
def search(request):
        q = request.GET['q']
        users = User.objects.filter(username__icontains = q)
        postss = Posts.objects.filter(inhalt__icontains = q)
        return render(request, 'search_results.html',
            {'users': users, 'postss' : postss,  'query': q})

class DeleteView(PostsName, DeleteView):
    template_name = 'delete_comfirm.html'
    success_url = '/home/'