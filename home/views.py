import logging
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db import transaction
from registration.forms import RegistrationForm
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from registration.backends.admin_approval.views import RegistrationView
from .forms import UserProfileForm, UserRegistrationForm

def index(request):
    logger1 = logging.getLogger(settings.PROJECTNANE + '.' + __name__)
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    context_dict = {'boldmessage': "No more crunchy, creamy, cookie, candy, cupcake! We will deal with syringes, needles, pills!"}
    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    logger1.info("context_dict: %s", context_dict)
    return render(request, 'home/index.html', context=context_dict)

@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('settings:profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = RegistrationForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.profile)
    return render(request, 'profiles/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


class MyRegistrationView(RegistrationView):

    form_class= UserRegistrationForm

    def register(self, request, **cleaned_data):
        return super(MyRegistrationView, self).register(request.registrationform, **cleaned_data)
    