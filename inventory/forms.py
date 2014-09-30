from django import forms
import datetime
from inventory.models import Experiment, Room, Material, Tag, Text, UserProfile, Resource, Image, Link
from django.contrib.auth.models import User
from django.utils.encoding import smart_str
from django.utils.safestring import mark_safe
from django.forms.util import flatatt

class CommaSeparatedWidget(forms.Widget):
    # See http://stackoverflow.com/questions/4960445/display-a-comma-separated-list-of-manytomany-items-in-a-charfield-on-a-modelform
    def render(self, name, value, attrs=None):
        final_attrs = self.build_attrs(attrs, type='text', name=name)
        
        if not type(value) == unicode:
            values = []
            for each in value:
                try:
                    values.append(str(Tag.objects.get(pk=each).name))
                except:
                    continue
            value = ', '.join(values)
            if value:
                final_attrs['value'] = smart_str(value)
                
        else:
            final_attrs['value'] = smart_str(value)
            
        return mark_safe(u'<input%s />' % flatatt(final_attrs))

class CommaSeparatedChoiceField(forms.ModelMultipleChoiceField):
    widget = CommaSeparatedWidget
    def clean(self, value):
        tag_list = []
        if value is not None:
            #value = [item.strip() for item in value.split(",")]
            for item in value.split(", "):
                tag_list.append(Tag.objects.get_or_create(name=item)[0].id)
        return super(CommaSeparatedChoiceField, self).clean(tag_list)
        
class LinkForm(forms.ModelForm):
    error_css_class = 'error'
    
    title = forms.CharField(help_text="Title")
    url = forms.CharField(help_text="Links")
    
    fields = ['title', 'url']
    
    class Meta:
        model = Link

class ImageForm(forms.ModelForm):
    error_css_class = 'error'
    
    caption = forms.CharField(help_text="Caption")
    path = forms.FileField(help_text="Images")
    
    fields = ['caption', 'path']
    
    class Meta:
        model = Image

class ResourceForm(forms.ModelForm):
    error_css_class = 'error'
    
    name = forms.CharField(help_text="Name")
    path = forms.FileField(help_text="Resources")
    
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
    on_program = forms.BooleanField(help_text="On Program?")
    tags = CommaSeparatedChoiceField(help_text="Tags", required=False, queryset=Tag.objects.all())
    complete = forms.BooleanField(help_text="Complete Page?", required=False)
    main_photo = forms.ImageField(help_text="Picture", required=False)
    
    fields = ['title', 'on_program', 'text', 'procedure', 'materials', 'resources', 'tags', 'complete', 'main_photo', 'resources']
    
    # An inline class to provide additional information on the form.
    class Meta:
        model = Experiment
        
    def save(self, commit=True):
        instance = super(ExperimentForm, self).save(commit=commit)
        tags = self.cleaned_data.get('self', None)
        if tags is not None:
            for tag_name in tags.split(", "):
                tag = Tag.objects.create(name=tag_name)
                instance.tags.add(tag)
        instance.save()
        return instance
        
        
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