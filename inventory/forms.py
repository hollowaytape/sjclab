from django import forms
import datetime
from inventory.models import Experiment, Room, Material, Tag, Text, UserProfile
from django.contrib.auth.models import User

class ExperimentForm(forms.ModelForm):
    error_css_class = 'error'
    
    title = forms.CharField(help_text="Title")
    text = forms.ModelChoiceField(help_text="Text", queryset=Text.objects.all())
    session = forms.IntegerField(help_text="Session", required=False)
    procedure = forms.CharField(widget=forms.Textarea, help_text="Procedure", required=False)
    materials = forms.ModelMultipleChoiceField(help_text="Materials", queryset=Material.objects.all(), required=False)
    resources = forms.FileField(help_text="Resources", required=False)
    on_program = forms.BooleanField(help_text="On Program?", required=False)
    tags = forms.ModelMultipleChoiceField(help_text="Tags", queryset=Tag.objects.all(), required=False)
    complete = forms.BooleanField(help_text="Complete Page?", required=False)
    main_photo = forms.ImageField(help_text="Picture", required=False)
    resources = forms.FileField(help_text="Resources", required=False)
    
    fields = ['title', 'on_program', 'text', 'session', 'procedure', 'materials', 'resources', 'tags', 'complete', 'main_photo', 'resources']
    
    # An inline class to provide additional information on the form.
    class Meta:
        model = Experiment
        
class RoomForm(forms.ModelForm):
    error_css_class = 'error'
    number = forms.IntegerField()
    
    class Meta:
        model = Room

class MaterialForm(forms.ModelForm):
    error_css_class = 'error'
    name = forms.CharField(help_text="Material")
    count = forms.IntegerField(help_text="Count")
    location = forms.CharField(help_text="Location")
    #room = forms.ModelChoiceField(help_text="Room", queryset=Room.objects.all())
    
    class Meta:
        model = Material
        exclude = ['room']

class TextForm(forms.ModelForm):
    error_css_class = 'error'
    title = forms.CharField(help_text="Text Name")
    author = forms.CharField(help_text="Author")
    manual = forms.CharField(help_text="Manual")  # Selects?
    year = forms.CharField(help_text="Year")      # Selects?
    
    class Meta:
        model = Text
        
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ()