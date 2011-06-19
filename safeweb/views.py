from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from forms import TravellerForm, process_secret, SafeForm, HelpForm, UpdateForm
from models import (Traveller, TravellerUpdate, HelpDetails, 
        STATUS_SAFE, STATUS_IN_DANGER, STATUS_IN_TRANSIT)
from safetrip.scripts import do_safe_actions, do_help_actions, do_update_actions
from safeweb.unique import get_name

def _get_unique_secret():
    attempt = get_name()
    try:
        Traveller.objects.get(secret=process_secret(attempt.lower()))
    except Traveller.DoesNotExist:
        return attempt
    return _get_unique_secret()

def register(request):
    if request.method == "POST":
        traveller_form = TravellerForm(request.POST, request.FILES)
        if traveller_form.is_valid():
            # combine traveller's secret with site secret and hash before saving
            traveller = traveller_form.save(commit=False)
            display_secret = _get_unique_secret()
            store_secret = process_secret(display_secret.lower())
            traveller.secret = store_secret
            traveller.save()

            initial_update = TravellerUpdate(traveller=traveller, 
                        status=STATUS_IN_TRANSIT, 
                        current_country=traveller.home_country)
            initial_update.save()
            return render_to_response('confirm.html',
                    {'secret': display_secret},
                    context_instance=RequestContext(request))
    else:
        traveller_form = TravellerForm()
    return render_to_response('register.html',
            {'traveller_form': traveller_form},
            context_instance=RequestContext(request))

def help(request, traveller_id=None, country=None):
    traveller = get_object_or_404(Traveller, pk=traveller_id)
    if not country:
        try:
            latest_update = TravellerUpdate.objects.filter(traveller=traveller).order_by('-updated')[0]
            country = latest_update.current_country
        except IndexError:
            country = traveller.destination_country
    # get latest update country, falling back to traveller's destination
    return render_to_response('help.html', {'traveller': traveller,
                'country': country},
                context_instance=RequestContext(request))

def update(request):
    if request.method == "POST":
        safe_form = SafeForm(data=request.POST)
        help_form = HelpForm(data=request.POST)
        update_form = UpdateForm(data=request.POST)
        if help_form.is_valid():
            data = help_form.cleaned_data
            traveller = data['traveller']
            update = TravellerUpdate(traveller=traveller,
                status=STATUS_IN_DANGER, 
                current_country=data['country'],
                update=data['help_message'])
            do_help_actions(traveller)
            kwargs = {'traveller_id': traveller.id}
            url_name = 'help'
            if data['country']:
                url_name = 'help-country'
                kwargs['country'] = data['country']
            return HttpResponseRedirect(reverse(url_name,
                    kwargs=kwargs))
        if safe_form.is_valid():
            traveller = safe_form.cleaned_data['traveller']
            update = TravellerUpdate(traveller=traveller,
                        status=STATUS_SAFE)
            update.save()
            do_safe_actions(traveller)
            return HttpResponseRedirect(reverse('safe'))
        if update_form.is_valid():
            data = update_form.cleaned_data
            traveller = data['traveller']
            update = TravellerUpdate(traveller=traveller,
                        status=STATUS_IN_TRANSIT, update=data['message'],
                        country=data['country'])
            do_update_actions(traveller)
            return HttpResponseRedirect(reverse('update'))
    else:
        safe_form = SafeForm()
        help_form = HelpForm()
        update_form = UpdateForm()
    return render_to_response('update.html',
            {'safe_form': safe_form,
            'help_form': help_form,
            'update_form': update_form},
            context_instance=RequestContext(request))

