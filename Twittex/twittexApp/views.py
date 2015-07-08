from pathlib import _Accessor
from django.db.models.query_utils import Q
from django.shortcuts import render, redirect, RequestContext, render_to_response, Http404
from itertools import chain
from django.db.models import Q
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView
from twittexApp.forms import UserCreationForm, AuthenticationForm, UserForm, UserProfileForm, PostsName, ListForm
from twittexApp.models import Posts, User, UserProfile, EmailForm, models, List, Conversation
from django.http import HttpResponse
import smtplib
from django.core.mail import send_mail
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth import authenticate


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

    # provide forms
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context
    return render_to_response(
        'register.html',
        {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
        context)


def ProfileDetailView(request, username):
    posts = Posts.objects.all().order_by('-datum')
    user = User.objects.get(username=username)
    follower= request.user.userprofile.follows.all()
    if len(follower) != 0 and user.userprofile in follower:
        follow= follower.get(user= user)
    else:
        follow = None

    privacy = 'yes'

    if username != request.user.username:
        if user.userprofile.privacy:
            if request.user.userprofile in user.userprofile.follows.all():
                privacy = 'yes'
            else:
                privacy = 'no'

    yes= 'yes'
    no= 'no'
    if follow is None :
        follow= 'no'
    else:
        follow = 'yes'
    return render_to_response('profile.html', {'object_list': posts, 'user': user, 'request': request, 'followlist': follower, 'follow':follow, 'privacy':privacy, 'yes': yes, 'no': no}, context_instance=RequestContext(request))


class ProfileEditView(UpdateView):
    template_name = 'editprofile.html'
    success_url = '/'
    fields = ['desc', 'picture', 'privacy']

    def get_object(self):
        return UserProfile.objects.get(user=self.request.user)


def viewList(request):
    list=List.objects.all()
    return render(request,'list.html',
    {'object_list': list})


def ListDetailView(request, pk):
    list = List.objects.get(id=pk)
    userlist = list.userlist.all()
    return render_to_response('listdetail.html', {'list': list, 'userlist': userlist,'request': request}, context_instance=RequestContext(request))


class NewListView(CreateView):
    template_name = 'newList.html'
    model = List
    success_url = '/followerlist/'
    form_class = ListForm


class ListEditView(UpdateView):
    template_name = 'editlist.html'
    fields = ['title', 'userlist']
    model = List

    def get_success_url(self):
        return reverse('twittexApp:list')


class ListDeleteView(DeleteView):
    template_name = 'delete_comfirm.html'
    success_url = '/home/'
    model = List


def ListFollowView(request, pk):
    list = List.objects.get(id = pk)
    userlist = list.userlist.all()
    for user in userlist:
        request.user.userprofile.follows.add(user.userprofile)
    return redirect('/home/')


# called by submit post
def newPost(request):
    content = str(request.POST.get('inhalt'))
    #hashtag search from http://stackoverflow.com/questions/6331497
    hashtags = set()
    mentioned = set()
    #links erkennen
    for tag in content.split():
        if tag.startswith("#"):
            strippedTag = tag.strip("#")
            hashtags.add(strippedTag)
            content = content.replace(tag, "<a href='/search/?q="+strippedTag+"'>"+tag+"</a>")
        if tag.startswith("@"):
            strippedTag = tag.strip("@")
            mentioned.add(strippedTag)
            content = content.replace(tag, "<a href='/profile/"+strippedTag+"'>"+tag+"</a>")
        if (tag.startswith("http://") | tag.startswith("https://")):
            content = content.replace(tag, "<a href='"+tag+"'>"+tag+"</a>")
        if tag.startswith("www."):
            content = content.replace(tag, "<a href='http://"+tag+"'>"+tag+"</a>")

    p = Posts(inhalt=content, hashtags=str(hashtags))
    p.autor = request.user
    p.save()

    for username in mentioned:
        user = User.objects.get(username=username)
        if (user.username == username):
            user.userprofile.mentioned_count += 1
            user.userprofile.save()
            p.mentioned.add(user)
            p.save()

    p.save()
    return redirect('/home/')


class DeleteView(PostsName, DeleteView):
    template_name = 'delete_comfirm.html'
    success_url = '/home/'


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

"""
#Nachrichten
class NewMsgView(ListView):
    template_name = 'newMsg.html'
    context_object_name = 'conversations'

    def get_queryset(self):
        usr = str(self.request.user)
        q = Nachrichten.objects.filter(Q(absender=usr)
                                       | Q(empfaenger=usr)).values('empfaenger').distinct(
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
                                                              | Q(empfaenger=usr)).values(
            'empfaenger').distinct('empfaenger')
        return context 
"""
def NachrichtenView(request):
    context_object_name = 'conversations'

    user = request.user
    eingang = Conversation.objects.filter(empfaenger=user).distinct('absender')
    ausgang = Conversation.objects.filter(absender=user).distinct('empfaenger')

    return render_to_response('nachrichten.html', {'eingang': eingang, 'ausgang': ausgang,'request': request}, context_instance=RequestContext(request))


def sendMsg(request):
    if request.method == 'POST':
        inhalt = request.POST['inhalt']
        empfaenger = request.POST['empfaenger']
        absender = request.user

        if not (User.objects.filter(username=empfaenger).exists()):
            # user not found
            return redirect('/home/')

        absender = User.objects.get(username=absender)
        empfaenger = User.objects.get(username=empfaenger)

        msg = Conversation(absender=absender, empfaenger=empfaenger, inhalt=inhalt)
        msg.save()

        return redirect('/messages/' + empfaenger.username)
    else:
        return render(request,
            'newMsg.html')


def ConversationView(request, username):
    mainuser = request.user

    if not (User.objects.filter(username=username).exists()):
        return redirect('/messages/')

    user = User.objects.get(username=username)
    lists = Conversation.objects.filter((Q(absender=mainuser) & Q(empfaenger=user)) | (Q(absender=user) & Q(empfaenger=mainuser))).order_by('-datum')
    return render_to_response('conversation.html', {'conversations': lists, 'request': request, 'partner': user}, context_instance=RequestContext(request))

def search(request):
        q = request.GET['q']
        users = User.objects.filter(username__icontains = q)
        postss = Posts.objects.filter(inhalt__icontains = q)
        userlist = postss.values_list('autor', flat=True)

        for user in userlist:
            print(user)

        for user in userlist:
            tmpuser = User.objects.get(id=user)

            if tmpuser.userprofile.privacy:
                # userlist = user.follows.all()
                if request.user.userprofile not in userlist:
                    postss = postss.exclude(autor=tmpuser)

        lists = List.objects.filter(title__icontains = q)
        return render(request, 'search_results.html',
            {'users': users, 'postss' : postss,  'query': q, 'lists': lists})


def viewHome(request): 
    postss=Posts.objects.all().order_by("-datum")
    name= request.user
    followers= request.user.userprofile.follows.all()
    noFollow= UserProfile.objects.all()
    for e in followers:
        us= e.user
        noFollow= noFollow.exclude(user=us)
    noFollow= noFollow.exclude(user=name)
    for a in noFollow:
        nam= a.user
        postss= postss.exclude(autor=nam)

    for follower in followers:
        if follower.privacy:
            userlist = follower.follows.all()
            if request.user.userprofile not in userlist:
                postss = postss.exclude(autor=follower.user)

    return render(request,'home.html',
    {'postss': postss})


def viewNotification(request):
    request.user.userprofile.mentioned_count = 0;
    request.user.userprofile.save()
    postss=Posts.objects.filter(mentioned=request.user)
    return render(request,'notification.html',
    {'postss': postss})


def following(request, username):
    userp= User.objects.get(username= username)
    request.user.userprofile.follows.add(userp.userprofile)
    return redirect('/profile/' +userp.username )


def unfollowing(request, username):
    userp= User.objects.get(username= username)
    request.user.userprofile.follows.remove(userp.userprofile)
    return redirect('/profile/' +userp.username )

#API
def apiPost(request):
    if request.method == "POST":
        usr = str(request.POST.get('username'))
        pswd = str(request.POST.get('password'))
        content = str(request.POST.get('inhalt'))
        user = authenticate(username=usr, password=pswd)
        if user is not None:
            return newPost(request)
        else:
            return HttpResponse('invalid user / pwd'+usr+pswd+content)
    else:
        return HttpResponse('Post method required')

class testApiView(CreateView):
    template_name = 'apiPost_test.html'
    
