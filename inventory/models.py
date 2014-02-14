from django.db import models
from django.contrib.auth.models import User
        
class Room(models.Model):
    number = models.IntegerField()
    
    def __unicode__(self):
        return str(self.number)

class Material(models.Model): 
    name = models.CharField(max_length=25)
    room = models.ForeignKey('Room', null=True, blank=True)
    location = models.CharField(max_length=100, default="Somewhere")
    count = models.IntegerField(default=1)        # Can't be like "2 pair".

    def __unicode__(self):
        return self.name
		
class Text(models.Model):
    YEAR_CHOICES = (
        ('FR', 'Freshman'),
        ('JR', 'Junior'),
        ('SR', 'Senior'),
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
	
    title = models.CharField(max_length=50)
    manual = models.CharField(max_length=30,
	                          choices=MANUAL_CHOICES, null=True, default='NULL')
    year = models.CharField(max_length=8,
                            choices=YEAR_CHOICES)
    author = models.CharField(max_length=20, null=True, default='Manual Authors')

    def __unicode__(self):
        return self.title
        
class Tag(models.Model):
    name = models.CharField(max_length=75)
    
    def __unicode__(self):
        return self.name


class Experiment(models.Model):
    title = models.CharField(max_length=200)
    text = models.ForeignKey('Text', null=True, blank=True)
    session = models.IntegerField(null=True, blank=True)
    procedure = models.TextField(null=True, blank=True)
    materials = models.ManyToManyField('Material', null=True, blank=True)
    # pictures, videos, pdfs.
    resources = models.FileField(upload_to=('/inventory/resources/'), null=True, blank=True)
    # on_program - is it a part of the manuals or official "sequence" of SJC? Then True.
    # If it's something the tutors/students came up with, then False.
    on_program = models.BooleanField(default=True)
    tags = models.ManyToManyField('Tag', null=True, blank=True)

    def __unicode__(self):
        return self.title
        
class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    picture = models.ImageField(upload_to='profile_images', blank=True)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username