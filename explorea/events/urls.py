from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('events/', views.event_listing, name='events'),
    path('runs/<int:pk>', views.event_runs, name='runs'),
    path('events/new/', views.create_event, name='create_event'),
    path('events/my_events/', views.my_events, name='my_events'),
    path('events/<int:event_id>/new_run/', views.create_event_run, name='create_event_run')
    # path('events/event01/', views.event01, name='event01'),
    # path('events/event02/', views.event02, name='event02'),
    # path('events/event03/', views.event03, name='event03'),
    # path('about/', views.about, name='about'),
    # path('event/<str:name>', views.event_detail, name='detail')
    			]