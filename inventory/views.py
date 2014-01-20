from django.template import RequestContext

from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from inventory.models import Experiment, Material, Text, Room

def url_safe(string):
    """ Replaces spaces with underscores, making a string safer for urls."""
    return string.replace(' ', '_')

def eye_safe(string):
    """ Undoes the operation of url_safe()."""
    return string.replace('_', ' ')

def experiment_index(request):
    # Obtain the context from the HTTP request.
    context = RequestContext(request)
    
    # Query the database for a list of all experiments.
    # Order the experiments by session in ascending order.
    # Place the list in our context_dict dictionary,
    # which will be passed to the template engine.
    experiment_list = Experiment.objects.order_by('session')
    context_dict = {'experiments': experiment_list}
    
    # Sanitize experiment names for use in urls.
    for experiment in experiment_list:
        experiment.url = experiment.title.replace(' ', '_')
    
    # Render the response and send it back!
    return render_to_response('inventory/experiment_index.html', context_dict, context)

    
def experiment(request, experiment_name_url):
    context = RequestContext(request)
    
    # Change underscores in the experiment name to spaces.
    experiment_name = experiment_name_url.replace('_', ' ')
    
    # Context dictionary to pass to the template.
    # Contain the name of the experiment passed by the user.
    context_dict = {'experiment_name': experiment_name}
    
    # Can we find an experiment with the given name?
    # If we can't, the .get() raises DoesNotExist.
    # SO the .get() method returns one model or raises an exception.
    experiment = get_object_or_404(Experiment, title=experiment_name)
    
    # Retrieve all of the experiment's materials.
    materials = experiment.materials
    
    # Create a list with the steps of the procedure separated.
    procedure = experiment.procedure.split('. ')
    
    # Add materials/procedure to the context dictionary.
    context_dict['materials'] = materials
    context_dict['procedure'] = procedure
    
    # Also add the experiment object.
    context_dict['experiment'] = experiment
    
    # Go render the response and return it to the client.
    return render_to_response('inventory/experiment.html', context_dict, context)