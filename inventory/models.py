from django.db import models
from django.contrib.auth.models import User
import datetime

class Image(models.Model):
    caption = models.CharField(max_length=100)
    path = models.ImageField(upload_to=('experiments/images/'))
    experiment = models.ForeignKey('Experiment', blank=True, null=True)
    
    def __unicode__(self):
        return self.caption
    
class Resource(models.Model):
    name = models.CharField(max_length=100)
    path = models.FileField(upload_to=('experiments/resources/'))
    experiment = models.ForeignKey('Experiment', blank=True, null=True)
    
    def __unicode__(self):
        return self.name
    
class Link(models.Model):
    title = models.CharField(max_length=200)
    url = models.CharField(max_length=400)
    experiment = models.ForeignKey('Experiment', blank=True, null=True)
    
    def __unicode__(self):
        return self.title

class Room(models.Model):
    floor = models.CharField(max_length=40, default="First Floor")
    hall = models.CharField(max_length=20, blank=True, null=True)
    number = models.CharField(max_length=20)    # Not quite a number, also things like "Music Library"
    date_modified = models.DateTimeField(default=datetime.datetime.now)
    
    def __unicode__(self):
        return self.number

class Material(models.Model): 
    name = models.CharField(max_length=100)
    room = models.ForeignKey('Room', null=True, blank=True)
    location = models.CharField(max_length=100, null=True, default="Somewhere")
    count = models.IntegerField(default=1)

    def __unicode__(self):
        return self.name
		
class Text(models.Model):
    YEAR_CHOICES = (
        ('FR', 'Freshman'),
        ('JR', 'Junior'),
        ('SR', 'Senior'),
        ('OT', 'Other'),
    )
	
    MANUAL_CHOICES = [
    ('OBSV', 'Observing Living Beings'),
	('EQLB', 'Measurement and Equilibrium'),
	('CONS', 'Constitution of Bodies'),
	
	('MECH', 'Mechanics'),
	('ELEC', 'Electricity and Magnetism'),
	('MXWL', 'Notes to Maxwell\'s Papers'),
	
	('ATOM', 'Atoms and Measurement'),
	('GENS', 'Genetics and Evolution')
	]
	
    title = models.CharField(max_length=100)
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
    title = models.CharField(max_length=200)
    text = models.ForeignKey('Text', null=True, blank=True)
    procedure = models.TextField(null=True, blank=True)
    materials = models.ManyToManyField('Material', null=True, blank=True)
    main_photo = models.ImageField(upload_to=('experiments/images/'), null=True, blank=True)
    resources = models.FileField(upload_to=('inventory/resources/'), null=True, blank=True)    # pdfs, videos, etc
    on_program = models.BooleanField(default=True)         # Is it in the text? Or did a tutor/assistant come up with it?
    complete = models.BooleanField(default=False)          # Mark true when all info filled out.
    tags = models.ManyToManyField('Tag', null=True, blank=True)

    def __unicode__(self):
        return self.title
        
class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username