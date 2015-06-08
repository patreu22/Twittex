from django.shortcuts import render, redirect, RequestContext, render_to_response
from django.views.generic import TemplateView, CreateView, ListView, DetailView
from twittexApp.forms import UserCreationForm, AuthenticationForm, UserForm, UserProfileForm
from twittexApp.models import Posts, User, UserProfile
from django.http import HttpResponse


# Create your views here.
class IndexView(TemplateView):
    template_name = 'index.html'


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
            print (user_form.errors, profile_form.errors)

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

class ProfileDetailView(TemplateView):
    template_name = 'profile.html'
    success_url = '/profile/'

#called by submit post
def newPost(request):
    p = Posts(absender = str(request.user), inhalt = str(request.POST.get('inhalt')), empfaenger ='NULL', hashtags='NULL', mentioned='NULL')
    p.save()
    return redirect('/home/')
