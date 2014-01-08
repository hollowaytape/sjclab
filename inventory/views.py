from django.template import RequestContext
from django.shortcuts import render_to_response
from baros.inventory import Experiment

def index(request):
	context = RequestContext(request)
	context_dict = {}
	return render_to_response('inventory/index.html', context_dict, context)