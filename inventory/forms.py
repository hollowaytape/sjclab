from django import forms
from inventory.models import Experiment, Room, Material, Tag, Text

class ExperimentForm(forms.ModelForm):
    error_css_class = 'error'
    
    title = forms.CharField(help_text="Title")
    text = forms.ModelChoiceField(help_text="Text", queryset=Text.objects.all())
    session = forms.IntegerField(help_text="Session")
    procedure = forms.CharField(widget=forms.Textarea, help_text="Procedure")
    materials = forms.ModelMultipleChoiceField(help_text="Materials", queryset=Material.objects.all())
    resources = forms.FileField(help_text="Resources")
    on_program = forms.BooleanField(help_text="On Program?")
    tags = forms.ModelMultipleChoiceField(help_text="Tags", queryset=Tag.objects.all())
    
    # An inline class to provide additional information on the form.
    class Meta:
        model = Experiment
        
class RoomForm(forms.ModelForm):
    number = forms.IntegerField()
    
    class Meta:
        model = Room
