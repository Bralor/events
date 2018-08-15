from django.urls import reverse_lazy
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Event, EventRun, Album, Image

from .forms import EventForm, EventRunForm, EventFilterForm, MultipleFileForm

from django.views.generic import ListView, DetailView
from django.views.generic.edit import DeleteView, CreateView


def index(request):
    ''' Main page, kind of welcome page with usefull text'''
    return render(request, 'events/index.html')


def event_listing(request, category=None):
	''' Basic offerings of events'''
	EventRuns	= EventRun.objects.all().filter_by_category(category)
	FilterForm 	= EventFilterForm(request.GET or None) # Only active events 
	
	if request.GET and FilterForm.is_valid():
		data = FilterForm.cleaned_data
	else:
		data = {}

	EventRuns 	= EventRuns.FirstFilter(**data)
	paginator 	= Paginator(EventRuns, 8) # Pagination settings
	page 		= request.GET.get('page')
	EventRuns 	= paginator.get_page(page)
	
	attributes 	= {'EventRuns': EventRuns, 'FilterForm': FilterForm}
	return render(request, 'events/event_listing.html', attributes)


class EventDetailView(DetailView):
	model 				= Event
	template_name 		= 'events/event_detail.html'
	context_object_name = 'event'

	def get_context_data(self, **kwargs):
		'''Insert the single object into the context dictionary.'''
		context = super().get_context_data(**kwargs)
		context['runs'] = self.object.ActiveRuns()
		return context


@login_required
def create_event(request):
	''' There is choice for the user to make his own event '''
	Form = EventForm(request.POST or None, request.FILES or None)

	if request.method == 'POST':
		if Form.is_valid():
			Form.cleaned_data.pop('gallery')
			event = Event.objects.create(host=request.user, **form.cleaned_data)

			# save the individual images
			for file in request.FILES.getlist('gallery'):
				Image.objects.create(album=event.album, image=file, title=file.name)

			return redirect(event.get_absolute_url())
	return render(request, 'events/create_event.html', {'Form': Form})


@login_required
def update_event(request, slug):
	'''New view of our update.html. It relates with create_event.view'''
	event = Event.objects.get(slug=slug)
	EvntForm = EventForm(request.POST or None, request.FILES or None, instance=event)
	FileForm = MultipleFileForm(files=request.FILES or None)

	if request.method == 'POST':
		if EvntForm.is_valid() and FileForm.is_valid():
			event = EvntForm.save()
			for file in request.FILES.getlist('gallery'):
				Image.objects.create(album=event.album, image=file, title=file.name)

			return redirect(event.get_absolute_url())
	return render(request, 'events/create_event.html', 
		{'EvntForm': EvntForm, 'FileForm': FileForm, 'event': event})


class MyEventsView(LoginRequiredMixin, ListView):
	# attributes
	context_object_name = 'events'
	template_name 		= 'events/my_events.html'

	def get_queryset(self):
		''' This method gets the data from database.'''
		return Event.objects.filter(host_id=self.request.user.id)


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


@login_required
def delete_event(request, slug):
	''' We want to terminate an event '''
	Event.objects.get(slug=slug).delete()
	return redirect('my_events')


class DeleteEventView(LoginRequiredMixin, DeleteView):
	model 		= Event
	success_url = reverse_lazy('events:my_events')


@login_required
def create_event_run(request, event_id):
	if request.method == 'POST':
		form = EventRunForm(request.POST)

		if form.is_valid():
			event_run = form.save(commit=False)
			event_run.event = Event.objects.get(pk=event_id)
			event_run.save()

			url = '/events/detail/{}'.format(event_id)
			return redirect(url)

	args = {'form': EventRunForm()}
	return render(request, 'events/create_event_run.html', args)


@login_required
def update_event_run(request, event_run_id):
	event_run = EventRun.objects.get(pk=event_run_id)
	if request.method == 'POST':
		form = EventRunForm(request.POST, instance=event_run)

		if form.is_valid():
			event_run = form.save()
			event_id  = event_run.event.id
			url  	  = '/events/detail/{}'.format(event_id)
			return redirect(url)

	return render(request, 'events/update_event_run.html',
		{'form': EventRunForm(instance=event_run)})


@login_required
def delete_event_run(request, event_run_id):
	run = EventRun.objects.get(pk=event_run_id)
	event_id = run.event.id
	run.delete()

	url = '/events/detail/{}'.format(event_id)
	return redirect(url)


def event_search(request):
	'''This view works with searchbar in header'''
	query 		= request.GET.get('q')
	events 		= Event.objects.search(query)
	FilterForm 	= EventFilterForm()
	paginator 	= Paginator(events, 16)
	page 		= request.GET.get('page')
	events 		= paginator.get_page(page)

	return render(request, 'events/event_listing.html', 
		{'events': events, 'FilterForm': FilterForm})
