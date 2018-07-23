from django.db import models
from django.conf import settings


# first model = class with events
class EventManager(models.Manager):
	'''This is a custom model that inherits all methods from models.Manager'''

	def filter_by_category(self, category):
		DbEquivalent = ''
		for shortcut in self.model.CATEGORY_CHOICES:
			if shortcut[1] == category:
				DbEquivalent = shortcut[0]
				break
		else:
			return self.all()
		return self.filter_by_category(category=DbEquivalent)


class Event(models.Model):
	'''docstring for ClassName'''
	FUN = 'FN'
	RELAX = 'RX'
	EXP = 'EX'
	SIGHTS = 'SI'

	CATEGORY_CHOICES = (
		(FUN, 'fun'),
		(RELAX, 'relax'),
		(EXP, 'experience'),
		(SIGHTS, 'sights')
						)

	host		= models.ForeignKey(settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE)
	name 		= models.CharField(max_length=200)
	description = models.TextField(max_length=1000)
	location 	= models.CharField(max_length=500)

	category 	= models.CharField(
		max_length=20,
		choices = CATEGORY_CHOICES,
		default = FUN,
									)
	objects = EventManager()

	def __str__(self):
		return self.name


class EventRun(models.Model):
	'''Little upgrade for our first method'''
	event 			= models.ForeignKey(Event,on_delete=models.CASCADE)
	date 			= models.DateField(blank=False, null=False)
	time 			= models.TimeField(blank=False, null=False)
	seats_available = models.PositiveIntegerField(blank=False, 
													null=False)
	price			= models.DecimalField(max_digits=10, decimal_places=2, 
											blank=False, null=False)

	def __str__(self):
		return self.event.name



