from django.shortcuts import render
from django.http import get_object_or_404()

from polls.inventory import Experiment

def index(request):
	experiment_list = Experiment.objects       # Can I get away with no order?
	context = {'experiment_list': experiment_list,}
	return render(request, 'inventory/inventory_index.html', context)

def experiment(request, experiment_id):
	experiment = get_object_or_404(Experiment, pk=experiment_id)
	return render(request, 'inventory/experiment.html', {'experiment' : experiment})