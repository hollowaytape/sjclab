from django.db import models
        
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
                            
    def __unicode__(self):
        return self.number
        
class Material(models.Model): 
    name = models.CharField(max_length=25)
    room = models.ManyToManyField(Room)
    location = models.CharField(max_length=100)
    count = models.IntegerField()        # Can't be like "2 pair".

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
	
    title = models.CharField(max_length=25)
    manual = models.CharField(max_length=4,
	                          choices=MANUAL_CHOICES, null=True, default='Null')
    year = models.CharField(max_length=2,
                            choices=YEAR_CHOICES)
    author = models.CharField(max_length=20, null=True, default='NULL')

    def __unicode__(self):
        return self.name
        
class Tag(models.Model):
    name = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.name


class Experiment(models.Model):
    title = models.CharField(max_length=200)
    text = models.CharField(max_length=50)
    procedure = models.TextField()
    materials = models.ManyToManyField(Material)
    resources = models.FileField(upload_to=('/%s/' % title))
    tags = models.ManyToManyField(Tag)

    def __unicode__(self):
        return self.title