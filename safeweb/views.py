from django.shortcuts import render_to_response
from django.template import RequestContext

def register(request):
    form = None
    return render_to_response('register.html',
            {'form': form},
            context_instance=RequestContext(request))

def update(request):
    form = None
    return render_to_response('update.html',
            {'form': form},
            context_instance=RequestContext(request))
