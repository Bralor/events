from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('events/', views.event_listing, name='events'),
    path('runs/', views.event_runs, name='runs'),
    # path('event/<str:name>', views.event_detail, name='detail')
    			]