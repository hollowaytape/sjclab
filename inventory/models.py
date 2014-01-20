from django.db import models
        
class Room(models.Model):
    number = models.IntegerField()
    
    def __unicode__(self):
        return str(self.number)

class Material(models.Model): 
    name = models.CharField(max_length=25)
    room = models.ForeignKey('Room', null=True, blank=True)
    location = models.CharField(max_length=100)
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
	
    title = models.CharField(max_length=25)
    manual = models.CharField(max_length=4,
	                          choices=MANUAL_CHOICES, null=True, default='NULL')
    year = models.CharField(max_length=2,
                            choices=YEAR_CHOICES)
    author = models.CharField(max_length=20, null=True, default='NULL')

    def __unicode__(self):
        return self.title


class Experiment(models.Model):
    title = models.CharField(max_length=200)
    text = models.ForeignKey('Text', null=True, blank=True)
    session = models.IntegerField(null=True, blank=True)
    procedure = models.TextField(null=True, blank=True)
    materials = models.ManyToManyField('Material', null=True, blank=True)
    resources = models.FileField(upload_to=('/inventory/resources/'), null=True, blank=True)
    tags = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.title