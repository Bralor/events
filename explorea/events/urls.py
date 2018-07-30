from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.event_listing, name='events'),
    path('new/', views.create_event, name='create_event'),
    path('my_events/', views.my_events, name='my_events'),
    path('search/', views.event_search, name='search'),
    
    path('detail/<slug:slug>/', views.event_detail, name='event_detail'),
    path('update/<slug:slug>/', views.update_event, name='update_event'),
    path('delete/<slug:slug>/', views.delete_event, name='delete_event'),
    
    path('<int:event_id>/new_run/', views.create_event_run, name='create_event_run'),
    path('update_run/<int:event_run_id>/', views.update_event_run,name='update_event_run'),
    path('delete_run/<int:event_run_id>/', views.delete_event_run,name='delete_event_run'),

    path('<category>/', views.event_listing, name='events_by_category'),
                ]