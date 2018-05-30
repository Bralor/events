from django.http import HttpResponse
from django.shortcuts import render
from .models import Event

# ORIGINAL MESSAGE -> Create your views here.

# def index(request):
# 	return HttpResponse("Hey Client, my app is running!")


def event_listing(request):
    ''' Main menu/offering of events in database.'''
    events = Event.objects.all()
    return render(request, 'event_listing.html', {'events': events})


def index(request):
    html = '''
    <p> Let's see some events: <a href="/events">detail</a></p>
    <ul>
    '''
    return render(request, 'index.html')
    return HttpResponse(html)
    
    
def event_detail(request, name):
    data = {
    	'Chill' : '<h2> Chill on the beach just for $400 </h2>',
    	'Camping': '<h2> Camp with us for $50 </h2>',
    	'Flying': '<h2> Fly for free </h2>'
    		}
    selection = data.get(name)

    if selection:
    	return HttpResponse(selection)
    else:
    	return HttpResponse('There is no such event in our offering')


