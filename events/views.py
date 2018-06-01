from django.http import HttpResponse
from django.shortcuts import render
from .models import Event, EventRun

# ORIGINAL MESSAGE -> Create your views here.

# def index(request):
# 	return HttpResponse("Hey Client, my app is running!")

def index(request):
    ''' Main menu. There is a link to the offering of events'''
    return render(request, 'index.html')


def event_listing(request):
    ''' Basic offerings'''
    events = Event.objects.all()
    return render(request, 'event_listing.html', {'events': events})


def event_runs(request):
    '''Here are some details like a date of the event'''
    runs = EventRun.objects.all()
    return render(request, 'event_runs.html', {'runs': runs})


def event01(request):
    '''Ahahaha'''
    events = Event.objects.all()
    runs = EventRun.objects.all()
    return render(request, 'event01.html', {'events': events})


def event02(request):
    return HttpResponse('Its actually running')


def event03(request):
    return HttpResponse('Its actually also running')


def about(request):
    return HttpResponse('Missing in action')


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


