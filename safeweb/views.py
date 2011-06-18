from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from forms import UserForm, UserProfileForm

def register(request):
    if request.method == "POST":
        user_form = UserForm(data = request.POST)
        profile_form = UserProfileForm(data = request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit = False)
            profile.user = user
            profile.save()
            return HttpResponseRedirect(reverse('post-register'))
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render_to_response('register.html',
            {'user_form': user_form, 'profile_form': profile_form},
            context_instance=RequestContext(request))

def update(request):
    """
    allow the user to change a subset of all their data
    """
    form = None
    return render_to_response('update.html',
            {'form': form},
            context_instance=RequestContext(request))
