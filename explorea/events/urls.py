from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('events/', views.event_listing, name='events'),
    path('runs/', views.event_runs, name='runs'),
    path('events/event01/', views.event01, name='event01'),
    path('events/event02/', views.event02, name='event02'),
    path('events/event03/', views.event03, name='event03'),
    path('about/', views.about, name='about'),
    # path('event/<str:name>', views.event_detail, name='detail')
    			]