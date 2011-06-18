from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from forms import TravellerForm

def process_secret(raw_secret):
    #TODO do this properly
    return raw_secret

def register(request):
    if request.method == "POST":
        traveller_form = TravellerForm(data=request.POST)
        if traveller_form.is_valid():
            # combine traveller's secret with site secret and hash before saving
            traveller = traveller_form.save(commit=False)
            traveller.secret = process_secret(traveller.secret)
            traveller.save()
            return HttpResponseRedirect(reverse('confirm'))
    else:
        traveller_form = TravellerForm()
    return render_to_response('register.html',
            {'traveller_form': traveller_form},
            context_instance=RequestContext(request))

def update(request):
    """
    allow the user to change a subset of all their data
    """
    form = None
    return render_to_response('update.html',
            {'form': form},
            context_instance=RequestContext(request))
