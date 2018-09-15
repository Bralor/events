from django import forms
from django.utils import timezone
from .models import Event, EventRun


class EventForm(forms.ModelForm):
    gallery = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), 
    	required=False)
    
    class Meta:
        model = Event
        exclude = ['host', 'slug']


class EventRunForm(forms.ModelForm):
	date = forms.DateField(input_formats=["%d.%m.%Y"], 
        widget=forms.DateInput(format = '%d.%m.%Y'))

	class Meta:
		model = EventRun
		exclude = ['event']


class EventFilterForm(forms.Form):
	'''This widget will help us to find our events'''
	DateFrom 	= forms.DateField(label="from", initial=None,
			widget=forms.SelectDateWidget, required=False)
	DateTo 		= forms.DateField(label="to", initial=None,
			widget=forms.SelectDateWidget, required=False)
	Guests 		= forms.IntegerField(required=False, min_value=1)

	def clean(self):
		super().clean()
		DateFrom 	= self.cleaned_data.get('DateFrom')
		DateTo 		= self.cleaned_data.get('DateTo')
		if ((DateFrom and DateTo) and DateFrom > DateTo):
			self.add_error('DateFrom', 'Your selected date is later than date to')

		for name, date in [('DateFrom', DateFrom), ('DateTo', DateTo)]:
			if date and date < timezone.now().date():
				self.add_error(name, 'You have selected date in the past')


class EventSearchFilterForm(EventFilterForm):
    
     q = forms.CharField(required=False, max_length=1000, initial='',
                                    widget=forms.HiddenInput())


