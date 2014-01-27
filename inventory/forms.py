from django import forms
from inventory.models import Experiment, Room, Material, Tag, Text

class ExperimentForm(forms.ModelForm):
    title = forms.CharField(max_length=200, help_text="Title")
    text = forms.CharField(max_length=200, help_text="Text")
    session = forms.IntegerField(help_text="Session")
    procedure = forms.CharField(max_length=2000, help_text="Procedure")
    materials = forms.CharField(max_length=400, help_text="Materials")
    resources = forms.FileField(help_text="Resources")
    on_program = forms.BooleanField(help_text="On Program?")
    tags = forms.CharField(max_length=200, help_text="Tags")
    
    # An inline class to provide additional information on the form.
    class Meta:
        model = Experiment
        
class RoomForm(forms.ModelForm):
    number = forms.IntegerField()
    
    class Meta:
        model = Room
