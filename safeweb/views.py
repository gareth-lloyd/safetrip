from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from forms import TravellerForm, process_secret, SafeForm, HelpForm

def register(request):
    if request.method == "POST":
        traveller_form = TravellerForm(request.POST, request.FILES)
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
    if request.method == "POST":
        safe_form = SafeForm(data=request.POST)
        help_form = HelpForm(data=request.POST)
        if safe_form.is_valid():
            processed_secret = safe_form.cleaned_data['safe_secret']
            traveller = get_traveller(processed_secret)
            traveller.status = STATUS_SAFE
            traveller.save()
            return HttpResponseRedirect(reverse('safe'))
        if help_form.is_valid():
            processed_secret = help_form.cleaned_data['help_secret']
            traveller = get_traveller(processed_secret)

            return HttpResponseRedirect(reverse('help'))
    else:
        safe_form = SafeForm()
        help_form = HelpForm()
    return render_to_response('update.html',
            {'safe_form': safe_form,
            'help_form': help_form},
            context_instance=RequestContext(request))
