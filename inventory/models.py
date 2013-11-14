from django.db import models

class Room(models.Model):
    number = models.IntegerField()
    type = models.CharField(max_length=15)  # Prep or class
    year = models.CharField(max_length=9) # F/J/S
	
    def __unicode__(self):
	    return self.number


class Material(models.Model): # Different counts in different places?
    name = models.CharField(max_length=50)
    room = models.ManyToManyField(Room)
    location = models.CharField(max_length=100)
	
	def __unicode__(self):
	    return self.name

class Tag(models.Model):
    name = models.CharField(max_length=30)
	
	def __unicode__(self):
	    return self.name

class Experiment(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=40)
    year = models.CharField(max_length=9)
    manual = models.CharField(max_length=50)
    procedure = models.CharField(max_length=1000)
    materials = models.ManyToManyField(Material)
    tags = models.ManyToManyField(Tag)
	
	def __unicode__(self):
	    return self.title

