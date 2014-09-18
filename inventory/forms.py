from django import forms
import datetime
from inventory.models import Experiment, Room, Material, Tag, Text, UserProfile, Resource, Image, Link
from django.contrib.auth.models import User

class LinkForm(forms.ModelForm):
    error_css_class = 'error'
    
    title = forms.CharField(help_text="Title")
    path = forms.CharField(help_text="Links", required=False)
    
    fields = ['title', 'path']
    
    class Meta:
        model = Link

class ImageForm(forms.ModelForm):
    error_css_class = 'error'
    
    caption = forms.CharField(help_text="Caption")
    path = forms.FileField(help_text="Images", required=False)
    
    fields = ['caption', 'path']
    
    class Meta:
        model = Image

class ResourceForm(forms.ModelForm):
    error_css_class = 'error'
    
    name = forms.CharField(help_text="Name")
    path = forms.FileField(help_text="Resources", required=False)
    
    fields = ['name', 'path']
    
    class Meta:
        model = Resource

class ExperimentForm(forms.ModelForm):
    error_css_class = 'error'
    
    title = forms.CharField(help_text="Title")
    text = forms.ModelChoiceField(help_text="Text", queryset=Text.objects.all().order_by('author'))
    procedure = forms.CharField(widget=forms.Textarea, help_text="Procedure", required=False)
    materials = forms.ModelMultipleChoiceField(help_text="Materials", queryset=Material.objects.all().order_by('name'), required=False)
    resources = forms.FileField(help_text="Resources", required=False)
    on_program = forms.BooleanField(help_text="On Program?", required=False)
    tags = forms.ModelMultipleChoiceField(help_text="Tags", queryset=Tag.objects.all(), required=False)
    complete = forms.BooleanField(help_text="Complete Page?", required=False)
    main_photo = forms.ImageField(help_text="Picture", required=False)
    
    fields = ['title', 'on_program', 'text', 'procedure', 'materials', 'resources', 'tags', 'complete', 'main_photo', 'resources']
    
    # An inline class to provide additional information on the form.
    class Meta:
        model = Experiment
        
class RoomForm(forms.ModelForm):
    error_css_class = 'error'
    number = forms.IntegerField()
    
    exclude = ['number']
    
    class Meta:
        model = Room

class MaterialForm(forms.ModelForm):
    error_css_class = 'error'
    name = forms.CharField(help_text="Material")
    count = forms.IntegerField(help_text="Count")
    location = forms.CharField(help_text="Location")
    
    fields = ['name', 'count', 'location']
    
    class Meta:
        model = Material

class TextForm(forms.ModelForm):
    error_css_class = 'error'
    title = forms.CharField(help_text="Text Name")
    author = forms.CharField(help_text="Author")
    manual = forms.CharField(help_text="Manual")  # Selects?
    year = forms.CharField(help_text="Year")      # Selects?
    
    fields = ['title', 'author', 'manual', 'year']
    
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