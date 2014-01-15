from django.contrib import admin
from inventory.models import Material, Text, Experiment

for model in (Material, Text, Experiment):
    admin.site.register(model)