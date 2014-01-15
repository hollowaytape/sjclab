from django.template import RequestContext
from django.shortcuts import render_to_response
from baros.inventory import Experiment, Material, Text

def index(request):
	# Obtain the context from the HTTP request.
    context = RequestContext(request)
    
    # Query the database for a list of all experiments.
    # Order the experiments by session in ascending order.
    # Place the list in our context_dict dictionary,
    # which will be passed to the template engine.
    experiment_list = Experiment.objects.order_by('session')
    context_dict = {'experiments': experiment_list}
    
    # Render the response and send it back!
    return render_to_response('inventory/experiment_index.html', context_dict, context)