from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Event, EventRun
from .forms import EventForm, EventRunForm
from django.contrib.auth.decorators import login_required


def index(request):
    ''' Main page, kind of welcome page with usefull text'''

    return render(request, 'index.html')


def event_listing(request):
    ''' Basic offerings of events'''

    events = Event.objects.all()
    return render(request, 'event_listing.html', {'events': events})


def event_runs(request):
	'''Here are some details like a date of the event'''

	event 	= Event.objects.all(pk=pk)
	runs 	= EventRun.objects.all()
	return render(request, 'event_runs.html', {'event': event, 'runs': runs})


@login_required
def create_event(request):
	''' There is choice for the user to make his own event '''

	if request.method == 'POST':
		form = EventForm(request.POST)
		if form.is_valid():
			event 		= form.save(commit=False)
			event.host 	= request.user
			event.save()
			return redirect('')

	form = EventForm()
	return render(request, 'create_event.html', {'form' : form})


@login_required
def my_events(request):
	'''I'm little bit confused about the purpose of this page'''

	events = Event.objects.filter(host_id=request.user.id)
	return render(request, 'my_events.html', {'events': events})


@login_required
def create_event_run(request, event_id):
	''' In case we want to add a new event run.'''

	if request.method == 'POST':
		form = EventRunForm(request.POST)

		if form.is_valid():
			event_run 		= form.save(commit=False)
			event_run.event = Event.objects.get(pk=event_id)
			event_run.save()

			url = 'events/detail/{}'.format(event_id)
			return redirect(url)
	return render(request, 'events/create_event_run.html', {'form': EventRunForm()})






