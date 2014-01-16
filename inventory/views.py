from django.template import RequestContext

from django.http import HttpResponse
from django.shortcuts import render_to_response
from inventory.models import Experiment, Material, Text
    
def experiment_index(request):
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

    
def experiment(request, experiment_name_url):
    context = RequestContext(request)
    
    # Context dictionary to pass to the template.
    # Contain the name of the experiment passed by the user.
    context_dict = {'experiment_name_url': experiment_name_url}
    
    try:
        # Can we find an experiment with the given name?
        # If we can't, the .get() raises DoesNotExist.
        # SO the .get() method returns one model or raises an exception.
        experiment = Experiment.objects.get(title_url=experiment_title_url)
        
        # Retrieve all of the experiment's materials.
        # TODO: Get the procedure's steps as well.
        exp_materials = experiment.materials.split(', ')
        materials = Material.objects.filter(name__in=exp_materials)
        
        # Adds our results list to the template context.
        context_dict['materials'] = materials
        
        # Also add the experiment object to the context dictionary.
        context_dict['experiment'] = experiment
        
    except Experiment.DoestNotExist:
        # Don't do anything.
        pass
    
    # Go render the response and return it to the client.
    return render_to_response('inventory/experiment.html', context_dict, context)