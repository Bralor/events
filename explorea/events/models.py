from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models import Max, F, Q


# first model = class with events
class EventQuerySet(models.QuerySet):
	'''This is a custom model that inherits all methods from models.Manager'''
	
	def filter_by_category(self, category):
		DbEquivalent = ''
		
		for shortcut in self.model.CATEGORY_CHOICES:
			if shortcut[1] == category:
				DbEquivalent = shortcut[0]
				break
		else:
			return self.all()
		
		return self.filter(category=DbEquivalent)

	
	def filter_available(self, DateFrom=None, DateTo=None, Guests=None):
		# 1. filter eventruns, 2. get IDs
		DateFrom = DateFrom or timezone.now().date()
		qs = self.annotate(max_seats=Max('eventrun__seats_available'))

		if DateTo:
			qs = EventRun.objects.filter(date__range=(DateFrom, DateTo))
		else:
			qs = EventRun.objects.filter(date__gte=DateFrom)

		if Guests:
			qs = qs.filter(seats_available__gte=Guests)

		return self.filter(pk__in=qs.values_list('event', flat=True))


class EventManager(models.Manager):
	def get_queryset(self):
		return EventQuerySet(self.model, using=self._db)


class Event(models.Model):
	FUN 	= 'FN'
	RELAX 	= 'RX'
	EXP 	= 'EX'
	SIGHTS 	= 'SI'

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

	class Meta:
		ordering = ['name']


class EventRun(models.Model):
	'''Little upgrade for our first method'''
	event 			= models.ForeignKey(Event,on_delete=models.CASCADE)
	date 			= models.DateField(blank=False, null=False)
	time 			= models.TimeField(blank=False, null=False)
	seats_available = models.PositiveIntegerField(blank=False, null=False)
	price			= models.DecimalField(max_digits=10, decimal_places=2, 
											blank=False, null=False)

	def __str__(self):
		return self.event.name

