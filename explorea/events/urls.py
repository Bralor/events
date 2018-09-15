from . import views
from django.urls import path

app_name = 'events'

urlpatterns = [
    path('new/', views.CreateEventView.as_view(), name='create_event'),
    path('my_events/', views.MyEventsView.as_view(), name='my_events'),
    path('search/', views.EventSearchView.as_view(), name='search'),
    
    path('detail/<slug:slug>/', views.EventDetailView.as_view(), name='event_detail'),
    path('update/<slug:slug>/', views.UpdateEventView.as_view(), name='update_event'),
    path('delete/<slug:slug>/', views.DeleteEventView.as_view(), name='delete_event'),
    
    path('<int:event_id>/new_run/', views.create_event_run, name='create_event_run'),
    path('update_run/<int:event_run_id>/', views.update_event_run,name='update_event_run'),
    path('delete_run/<int:event_run_id>/', views.delete_event_run,name='delete_event_run'),

    path('<category>/', views.EventListView.as_view(), name='events'),
                ]