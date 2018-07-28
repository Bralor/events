from django import forms
from .models import Event, EventRun


class EventForm(forms.ModelForm):
	class Meta:
		model = Event
		exclude = ['host']


class EventRunForm(forms.ModelForm):
	date = forms.DateField(input_formats=["%d.%m.%Y"], 
        widget=forms.DateInput(format = '%d.%m.%Y'))

	class Meta:
		model = EventRun
		exclude = ['event']


class EventFilterForm(forms.Form):
	'''This widget will help us to find our events '''
	DateFrom 	= forms.DateField(label="from", initial=None,
			widget=forms.SelectDateWidget, required=False)
	DateTo 		= forms.DateField(label="to", initial=None,
			widget=forms.SelectDateWidget, required=False)
	Guests 		= forms.IntegerField(required=False, min_value=1)		






