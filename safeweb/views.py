from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from forms import TravellerForm, process_secret, SafeForm, HelpForm
from models import Traveller, STATUS_SAFE, STATUS_IN_DANGER
from safetrip.scripts import do_safe_actions, do_help_actions
from safeweb.unique import get_name

def register(request):
    if request.method == "POST":
        traveller_form = TravellerForm(request.POST, request.FILES)
        if traveller_form.is_valid():
            # combine traveller's secret with site secret and hash before saving
            traveller = traveller_form.save(commit=False)
            display_secret = get_name()
            store_secret = process_secret(display_secret.lower())
            traveller.secret = store_secret
            traveller.save()
            return render_to_response('confirm.html',
                    {'secret': display_secret},
                    context_instance=RequestContext(request))
    else:
        traveller_form = TravellerForm()
    return render_to_response('register.html',
            {'traveller_form': traveller_form},
            context_instance=RequestContext(request))

def update(request):
    if request.method == "POST":
        safe_form = SafeForm(data=request.POST)
        help_form = HelpForm(data=request.POST)
        if help_form.is_valid():
            traveller = help_form.cleaned_data['traveller']
            traveller.status = STATUS_IN_DANGER
            traveller.save()
            do_help_actions(traveller)
            return HttpResponseRedirect(reverse('help'))
        if safe_form.is_valid():
            traveller = safe_form.cleaned_data['traveller']
            traveller.status = STATUS_SAFE
            traveller.save()
            do_safe_actions(traveller)
            return HttpResponseRedirect(reverse('safe'))
    else:
        safe_form = SafeForm()
        help_form = HelpForm()
    return render_to_response('update.html',
            {'safe_form': safe_form,
            'help_form': help_form},
            context_instance=RequestContext(request))
