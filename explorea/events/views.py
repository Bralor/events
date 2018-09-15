from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Event, EventRun, Album, Image

from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView, FormMixin
from django.views.generic.edit import DeleteView, CreateView, UpdateView

from .forms import EventForm, EventRunForm, EventFilterForm, EventSearchFilterForm


def index(request):
    ''' Main page, kind of welcome page with usefull text'''
    return render(request, 'events/index.html')


class GetFormMixin(FormMixin):

	def get_form_kwargs(self):
		kwargs = {
			'initial': self.get_initial(),
			'prefix': self.get_prefix(),
			'data': self.request.GET,
			}
		return kwargs
		

class EventListView(GetFormMixin, ListView):
    model 				= EventRun
    context_object_name = 'EventRuns'
    form_class 			= EventFilterForm
    template_name 		= 'events/event_listing.html'
    paginate_by 		= 4

    def get(self, request, *args, **kwargs):
    	self.form = self.get_form()
    	if self.form.is_valid():
    		return super().get(request, *args, **kwargs)
    	self.object_list = []
    	return self.form_invalid(self.form)

    def get_queryset(self):
        qs = self.model._default_manager.all().filter_by_category(self.kwargs['category'])
        return qs.FirstFilter(**self.form.cleaned_data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['FilterForm'] = self.form
        return context


class EventDetailView(DetailView):
	model 				= Event
	template_name 		= 'events/event_detail.html'
	context_object_name = 'event'

	def get_context_data(self, **kwargs):
		'''Insert the single object into the context dictionary.'''
		context = super().get_context_data(**kwargs)
		context['runs'] = self.object.ActiveRuns()
		return context


class CreateEventView(LoginRequiredMixin, CreateView):
	model 			= Event
	form_class 		= EventForm
	template_name 	= 'events/create_event.html'

	def form_valid(self, form):
		form.cleaned_data.pop('gallery')
		event = Event.objects.create(host=self.request.user, **form.cleaned_data)

		# save the individual images
		for file in self.request.FILES.getlist('gallery'):
			Image.objects.create(album=event.album, image=file, title=file.name)

		return redirect(event.get_absolute_url())


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


class UpdateEventView(LoginRequiredMixin, UpdateView):
	model 			= Event
	form_class 		= EventForm
	template_name 	= 'events/create_event.html'

	def form_valid(self, form):
		event = form.save()

		# save the individual images
		for file in self.request.FILES.getlist('gallery'):
			Image.objects.create(album=event.album, image=file, title=file.name)

		return redirect(event.get_absolute_url())


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


# @login_required
# def create_event_run(request, event_id):
# 	if request.method == 'POST':
# 		form = EventRunForm(request.POST)

# 		if form.is_valid():
# 			event_run = form.save(commit=False)
# 			event_run.event = Event.objects.get(pk=event_id)
# 			event_run.save()

# 			url = '/events/detail/{}'.format(event_id)
# 			return redirect(url)

# 	args = {'form': EventRunForm()}
# 	return render(request, 'events/create_event_run.html', args)

@login_required
def create_event_run(request, event_id):
	if request.method == 'POST':
		form = EventRunForm(request.POST)

		if form.is_valid():
			event_run = form.save(commit=False)
			event_run.event = Event.objects.get(pk=event_id)
			event_run.save()
			messages.success(request, 'The run has been created successfully')
			return redirect(event_run.event.get_absolute_url())
		
		else:
			messages.error(request, 'The run could not be created')

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


class EventSearchView(ListView):
	'''This class-based view works with searchbar in header'''
	model 				= EventRun
	form_class 			= EventSearchFilterForm
	template_name 		= 'events/event_listing.html'
	paginate_by 		= 4
	context_object_name = 'EventRuns'
	#extra_context 		= {'FilterForm': EventFilterForm()}

	def get(self, request, *args, **kwargs):
		self.form = self.get_form()
		if self.form.is_valid():
			self.query = self.form.cleaned_data.pop('q')
			return super().get(request, *args, **kwargs)

		self.object_list = []
		return self.form_invalid(self.form)

	def get_queryset(self):
		qs =  self.model._default_manager.search(self.query)
		return qs.FirstFilter(**self.form.cleaned_data)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['FilterForm'] = self.form
		return context
