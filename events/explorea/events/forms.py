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

