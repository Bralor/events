import re
from django.core.exceptions import ValidationError


def validate_human_name(value):
	'''
	This validator checks if the inputed name contains only letters,
	spaces and dashes
	'''
	regex = r'^[A-Za-z\s\-]+$'
	# We will use a function of module re, match()
	if not re.match(regex, value):
		raise ValidationError(
				'Names can contain only alpha characters',
			code='invalid')	