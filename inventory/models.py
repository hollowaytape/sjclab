from django.db import models

class Material(models.Model): 
    name = models.CharField(max_length=25)
    room = models.IntegerField()
    location = models.CharField(max_length=100)
    count = models.IntegerField()
	
    def __unicode__(self):
        return self.name
		
class Text(models.Model):
    YEAR_CHOICES = (
        ('FR', 'Freshman'),
        ('JR', 'Junior'),
        ('SR', 'Senior'),
    )
	
    MANUAL_CHOICES = [               # Freshman only so far.
	('OLB', 'Observing Living Beings'),
	('ME', 'Measurement and Equilibrium'),
	('CB', 'Constitution of Bodies')
	]
	
    title = models.CharField(max_length=25)
    manual = models.CharField(max_length=50,
	                          choices=MANUAL_CHOICES)
    year = models.CharField(max_length=2,
                            choices=YEAR_CHOICES)
    author = models.CharField(max_length=20)

    def __unicode__(self):
        return self.title


class Experiment(models.Model):
    title = models.CharField(max_length=200)
    text = models.CharField(max_length=50)
    procedure = models.TextField()
    materials = models.ManyToManyField(Material)
	# resources = models.FileField(upload_to=('/%s/' % self.title))
    tags = models.TextField()

    def __unicode__(self):
        return self.title

# The procedure is so long-winded that it may not be suited for a database.
# Tags may need to have their own table, depending on how SQLite handles many-to-manys.
# Or maybe there's a list-field?
# Need to figure out proper syntax for the FileField.