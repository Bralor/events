from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Event, EventRun
from .forms import EventForm, EventRunForm


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


def my_events(request):
	'''I'm little bit confused about the purpose of this page'''
	events = Event.objects.filter(host_id=request.user.id)
	return render(request, 'my_events.html', {'events': events})


# def event01(request):
#     '''Ahahaha'''
#     events = Event.objects.all()
#     runs = EventRun.objects.all()
#     return render(request, 'event01.html', {'events': events})


# def event02(request):
#     return HttpResponse('Its actually running')


# def event03(request):
#     return HttpResponse('Its actually also running')


# def about(request):
#     return HttpResponse('Missing in action')


# def event_detail(request, name):
#     data = {
#     	'Chill' : '<h2> Chill on the beach just for $400 </h2>',
#     	'Camping': '<h2> Camp with us for $50 </h2>',
#     	'Flying': '<h2> Fly for free </h2>'
#     		}
#     selection = data.get(name)

#     if selection:
#     	return HttpResponse(selection)
#     else:
#     	return HttpResponse('There is no such event in our offering')


