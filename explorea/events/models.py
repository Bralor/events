from django.db import models

# Create your models here.
# first model = class with events
class Event(models.Model):
	'''docstring for ClassName'''
	name        = models.CharField(max_length = 200)
	description = models.TextField(max_length = 200)
	location	= models.CharField(max_length = 500)
	category	= models.CharField(max_length = 20)

	def __str__(self):
		return self.name


class EventRun(models.Model):
	'''Little upgrade for our first method'''
	event 			= models.ForeignKey(Event,on_delete=models.CASCADE)
	happens			= models.DateTimeField(blank=False, null=False)
	seats_available = models.PositiveIntegerField(blank=False, null=False)
	price			= models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)

	def __str__(self):
		return self.event.name