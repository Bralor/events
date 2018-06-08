from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = 	[
	path('profile/', views.profile, name='profile'),
	path('login/', auth_views.login, {'template_name': 'accounts/login.html'}, name='login')
				]