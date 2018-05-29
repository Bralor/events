from django.db import models

# Create your models here.
# first model = class with events
class Event(models.Model):
	"""docstring for ClassName"""
	name        = models.CharField(max_length = 200)
	description = models.TextField(max_length = 200)
	location	= models.CharField(max_length = 500)
	category	= models.CharField(max_length = 20)
