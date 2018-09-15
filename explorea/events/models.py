from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from django.db.models import Max, F, Q
from django.utils.text import slugify
# hint: these are not the django.(features) 
# better to start a whole new block
from imagekit.processors import ResizeToFill
from imagekit.models import ProcessedImageField


def thumbnail_image_url(instance, filename):
    '''upload_to for Event thumbnail image'''
    return 'user_{0}/thumb_{1}'.format(instance.host.id, filename) 


def main_image_url(instance, filename):
    '''upload_to for Event main image'''
    return 'user_{0}/main_{1}'.format(instance.host.id, filename)


def album_image_url(instance, filename):
	'''upload_to for Image model'''
	return 'user_{0}/{1}/{2}'.format(instance.album.event.host.id,
		instance.album.title, filename)


# first model = class with events
class EventQuerySet(models.QuerySet):
	'''This is a custom model that inherits all methods from models.Manager'''
	
	def filter_by_category(self, category=None):
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

	def search(self, query=None):
		''' Our searchbar is looking in these three categories'''
		lookup = (
			Q(name__icontains=query) |
			Q(description__icontains=query) |
			Q(location__icontains=query)
				)
		return self.filter(lookup).distinct()


class EventRunQuerySet(models.QuerySet):

	def filter_by_category(self, category=None):
		DbEquivalent = ''
		for shortcut in Event.CATEGORY_CHOICES:
			if shortcut[1] == category:
				DbEquivalent = shortcut[0]
				break
		else:
			return self.all()
		return self.filter(event__category=DbEquivalent)


	def filter_available(self, DateFrom=None, DateTo=None, Guests=None):
		DateFrom = DateFrom or timezone.now().date()
		if DateTo:
			qs = self.filter(date__range=(DateFrom, DateTo))
		else:
			qs = self.filter(date__gte=DateFrom)

		if Guests:
			qs = qs.filter(seats_available__gte=Guests)
		return qs


	def FirstFilter(self, DateFrom=None, DateTo=None, Guests=None):
		qs = self.filter_available(DateFrom, DateTo, Guests).order_by('date', 'time')
		EventIds = []
		Filtered=[]

		for run in qs:
			if not run.event.id in EventIds:
				Filtered.append(run)
				EventIds.append(run.event.id)
		return Filtered


class EventRunManager(models.Manager):
	'''class based view instead of event_listing view'''

	def get_queryset(self):
		return EventRunQuerySet(self.model, using=self._db)

	def search(self, query=None):
		lookup = (
			Q(event__name__icontains=query) |
			Q(event__description__icontains=query) |
			Q(event__location__icontains=query)
				)
		return self.filter(lookup).distinct()


class Event(models.Model):
	'''Method for Event DB creation'''
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
	slug 		= models.SlugField(max_length=200, unique=True, null=True)
	description = models.TextField(max_length=1000)
	location 	= models.CharField(max_length=500)
	created 	= models.DateTimeField(auto_now_add=True, null=True)
	thumbnail = ProcessedImageField(
		upload_to=thumbnail_image_url,
		processors=[ResizeToFill(300,200)],
		format='PNG',
		options={'quality':60},
		null=True)
	main_image = ProcessedImageField(
		upload_to=main_image_url,
		processors=[ResizeToFill(500,600)],
		format='PNG',
		options={'quality':100},
		null=True)
	category = models.CharField(
		max_length=20,
		choices = CATEGORY_CHOICES,
		default = FUN,
								)
	objects = EventManager()

	def __str__(self):
		return self.name

	class Meta:
		ordering 		= ['name']
		unique_together = (("name", "host"),)

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.name + '-with-' + self.host.username)
		super().save(*args, **kwargs)

		if not hasattr(self, 'album'):
			Album.objects.create(event=self)

	def ActiveRuns(self):
		today = timezone.now().date()
		return self.eventrun_set.filter(date__gte=today)

	def get_absolute_url(self):
		''' url generator'''
		return reverse('events:event_detail', args=[self.slug])


class EventRun(models.Model):
	'''Little upgrade for our first method'''
	event 			= models.ForeignKey(Event,on_delete=models.CASCADE)
	date 			= models.DateField(blank=False, null=False)
	time 			= models.TimeField(blank=False, null=False)
	seats_available = models.PositiveIntegerField(blank=False, null=False)
	price			= models.DecimalField(max_digits=10, decimal_places=2, 
											blank=False, null=False)
	objects = EventRunManager()

	def __str__(self):
		return self.event.name

	class Meta:
		ordering = ['date', 'time']



class Album(models.Model):
	'''aaaa'''
	event 	= models.OneToOneField(Event, on_delete=models.CASCADE)
	title 	= models.CharField(max_length=200, null=True)
	created = models.DateTimeField(auto_now_add=True)

	def save(self, *args, **kwargs):
		if not self.title:
			self.title = "album_" + self.event.name
		super().save(*args, **kwargs)

	def __str__(self):
		return '{}'.format(self.title)


class Image(models.Model):
	'''aaa'''
	album 	= models.ForeignKey(Album, on_delete=models.CASCADE)
	image 	= ProcessedImageField(upload_to=album_image_url,
		processors=[ResizeToFill(500,400)],
		format='PNG',
		options={'quality':80})
	title 	= models.CharField(max_length=200, null=True)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return '{}/{}'.format(self.album, self.title)

	class Meta:
		ordering = ['created']

