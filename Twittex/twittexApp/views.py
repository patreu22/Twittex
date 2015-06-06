from django.shortcuts import render, redirect, RequestContext, render_to_response
from django.views.generic import TemplateView, CreateView, ListView, DetailView
from twittexApp.forms import UserCreationForm, AuthenticationForm, UserForm, UserProfileForm
from twittexApp.models import Posts, User, UserProfile
from django.http import HttpResponse


# Create your views here.
class IndexView(TemplateView):
    template_name = 'index.html'

"""
class RegisterView(CreateView):
    template_name = 'register.html'
    model = UserProfile
    success_url = '/login/'
    form_class = UserCreationForm
"""

def register(request):
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print (user_form.errors, profile_form.errors)

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
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

class ProfileView(TemplateView):
    template_name = 'profile.html'
    success_url = '/profile/'
	
#called by submit post
def newPost(request):
    p = Posts(absender = str(request.user), inhalt = str(request.POST.get('inhalt')), empfaenger ='NULL', hashtags='NULL', mentioned='NULL')
    p.save()
    return redirect('/home/')
