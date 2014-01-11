from django.db import models

class Material(models.Model): 
    name = models.CharField(max_length=25)
    room = models.IntegerField()
    location = models.CharField(max_length=100)
    count = models.IntegerField()        # Can't be like "2 pair".
	
    def __init__(self, name):
        self.name = name

    def __unicode__(self, name=None):
	if name is None:
	    name = self.name
	    return name
        
class Room(models.Model):
    YEAR_CHOICES = (
        ('FR', 'Freshman'),
        ('JR', 'Junior'),
        ('SR', 'Senior'),
    )
    
    TYPE_CHOICES = (
        ('P', 'Prep'),
        ('C', 'Class'),
    )
    
    number = models.IntegerField()
    year = models.CharField(max_length=2,
                            choices=YEAR_CHOICES)
    type = models.CharField(max_length=1,
                            choices=TYPE_CHOICES)
		
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
	
    title = models.CharField(max_length=25)
    manual = models.CharField(max_length=4,
	                          choices=MANUAL_CHOICES, null=True, default='Null')
    year = models.CharField(max_length=2,
                            choices=YEAR_CHOICES)
    author = models.CharField(max_length=20, null=True, default='NULL')

    def __init__(self, title):
        self.title = title

    def __unicode__(self, title=None):
	if title is None:
	    title = self.title
	    return title


class Experiment(models.Model):
    title = models.CharField(max_length=200)
    text = models.CharField(max_length=50)
    procedure = models.TextField()
    materials = models.ManyToManyField(Material)
    resources = models.FileField(upload_to=('/%s/' % title))
    tags = models.TextField()

    def __init__(self, title):
        self.title = title

    def __unicode__(self, title=None):
	if title is None:
	    title = self.title
	    return title