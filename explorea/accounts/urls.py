from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = 	[
	path('login/', auth_views.login, {'template_name': 'accounts/login.html'}, name='login'),
	path('logout/', auth_views.logout, {'template_name': 'accounts/logged_out.html'}, name='logout'),
	path('register/', views.register, name='register'),
	path('profile/', views.profile, name='profile'),
	path('profile/edit/', views.edit_profile, name='edit_profile'),
				]