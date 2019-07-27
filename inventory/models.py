from django.db import models
from django.contrib.auth.models import User
from django.core.validators import URLValidator
import datetime

def validate_filesize(fieldfile_obj):
    filesize = fieldfile_obj.file.size
    megabyte_limit = 5.0
    if filesize > megabyte_limit*1024*1024:
        raise ValidationError("Max file size is %sMB" % str(megabyte_limit))

class Image(models.Model):
    caption = models.CharField(max_length=100)
    path = models.ImageField(upload_to=('experiments/images/'), validators=[validate_filesize])
    experiment = models.ForeignKey('Experiment', blank=True, null=True, on_delete="SET_NULL") 
    
    def __unicode__(self):
        return self.caption
    
class Resource(models.Model):            
    name = models.CharField(max_length=100)
    path = models.FileField(upload_to=('experiments/resources/'), validators=[validate_filesize])
    experiment = models.ForeignKey('Experiment', blank=True, null=True, on_delete="SET_NULL")
    
    def __unicode__(self):
        return self.name
    
class Link(models.Model):
    title = models.CharField(max_length=200)
    url = models.CharField(max_length=400, validators=[URLValidator()])
    experiment = models.ForeignKey('Experiment', blank=True, null=True, on_delete="SET_NULL")

    def __unicode__(self):
        return self.title


class Room(models.Model):
    floor = models.CharField(max_length=40, default="First Floor")
    hall = models.CharField(max_length=20, blank=True, null=True)
    # Not always a number, also things like "Music Library"
    number = models.CharField(max_length=20)
    date_modified = models.DateTimeField(default=datetime.datetime.now)
    
    def __unicode__(self):
        return self.number


class Material(models.Model): 
    name = models.CharField(max_length=100)
    room = models.ForeignKey('Room', null=True, blank=True, on_delete="SET_NULL")
    location = models.CharField(max_length=100, blank=True, null=True, default="Somewhere")
    count = models.IntegerField(default=1)

    def __unicode__(self):
        return self.name


class Text(models.Model):

    YEAR_CHOICES = (
        ("Freshman", 'Freshman'),
        ("Junior", 'Junior'),
        ("Senior", 'Senior'),
        ("Other", 'Other'),
    )

    MANUAL_CHOICES = [
    ("Observing Living Beings", 'Observing Living Beings'),
    ("Measurement and Equilibrium", 'Measurement and Equilibrium'),
    ("Constitution of Bodies", 'Constitution of Bodies'),

    ("Mechanics", 'Mechanics'),
    ("Electricity and Magnetism", 'Electricity and Magnetism'),
    ("Maxwell's Papers", "Maxwell's Papers"),

    ("Atoms and Measurement", 'Atoms and Measurement'),
    ("Genetics and Evolution", 'Genetics and Evolution')
    ]

    title = models.CharField(max_length=100, unique=True)
    manual = models.CharField(max_length=30, choices=MANUAL_CHOICES, null=True, default='NULL')
    year = models.CharField(max_length=8, choices=YEAR_CHOICES)
    author = models.CharField(max_length=80, null=True, default='Manual Authors')

    def __unicode__(self):
        return "%s, %s" % (self.author, self.title)


class Tag(models.Model):
    name = models.CharField(max_length=75)
    
    def __unicode__(self):
        return self.name


class Experiment(models.Model):
    title = models.CharField(max_length=200, unique=True)
    text = models.ForeignKey('Text', null=True, blank=True, on_delete="SET_NULL")
    procedure = models.TextField(null=True, blank=True)
    materials = models.ManyToManyField('Material', null=True, blank=True)
    main_photo = models.ImageField(upload_to=('experiments/images/'), null=True, blank=True)
    resources = models.FileField(upload_to=('inventory/resources/'), null=True, blank=True)
    # Is it in the manual/text? True. Is it something a tutor came up with? False.
    on_program = models.BooleanField(default=True)
    # Mark complete when the page has a reasonable amount of info.
    complete = models.BooleanField(default=False)
    tags = models.ManyToManyField('Tag', null=True, blank=True)

    def __unicode__(self):
        return self.title
        
    def get_tags(self):
        return "".join([t.name for t in self.tags.all()])


class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User, on_delete="SET_NULL")

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username